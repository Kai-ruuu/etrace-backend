import sys
import asyncio
import subprocess

from app.models.all import *
from app.utils.logging import Logger
from app.core.enums import AccountRole
from app.core.database import AsyncSessionLocal
from app.schemas.course import CourseIn
from app.schemas.school import SchoolIn
from app.schemas.account import DeanAccountIn, PesoStaffAccountIn
from app.services.course import CourseService
from app.services.school import SchoolService
from app.services.account_provision import AccountProvisionService


class Seeder:
    async def seed_system_admin(self, db) -> Account:
        service = AccountProvisionService(db, AccountRole.SYSTEM_ADMIN)
        return await service.bootstap_default_system_admin()
        

    async def seed_school(self, db, system_admin_account: Account) -> School:
        service = SchoolService(db)
        return await service.create(
            user=system_admin_account,
            school=SchoolIn(name="School of Computer Studies")
        )
        

    async def seed_course(self, db, dean_account: Account) -> Course:
        service = CourseService(db)
        return await service.create(
            user=dean_account,
            course=CourseIn(name="Bachelor of Science in Computer Science")
        )
        

    async def seed_dean(self, db, system_admin_account: Account, school_id: int) -> Account:
        service = AccountProvisionService(db, AccountRole.DEAN)
        account, _ = await service.create_dean(
            user=system_admin_account,
            dean=DeanAccountIn(
                email="dean@email.com",
                first_name="Dean",
                last_name="Administrator",
                school_id=school_id,
            ),
            as_pymodel=False,
            dev_setup_password="deanpass"
        )
        return account
        

    async def seed_peso_staff(self, db, system_admin_account: Account) -> Account:
        service = AccountProvisionService(db, AccountRole.PESO_STAFF)
        return await service.create_peso_staff(
            user=system_admin_account,
            peso_staff=PesoStaffAccountIn(
                email="peso@email.com",
                first_name="PESO",
                last_name="Staff",
            ),
            as_pymodel=False,
            dev_setup_password="pesopass"
        )


    async def seed(self):
        Logger.info("Seeding users...")

        async with AsyncSessionLocal() as db:
            system_admin = await self.seed_system_admin(db)
            school = await self.seed_school(db, system_admin)
            dean = await self.seed_dean(db, system_admin, school.id)
            await self.seed_course(db, dean)
            await self.seed_peso_staff(db, system_admin)

        Logger.success("Seeded users.")
        

    def create_tables(self) -> None:
        Logger.info("Creating database tables...")
        subprocess.run(["alembic", "upgrade", "head"])
        Logger.success("Created tables.")


async def main():
    seeder = Seeder()
    seeder.create_tables()
    await seeder.seed()

if __name__ == "__main__":
    run_after = "-r" in sys.argv
    
    asyncio.run(main())

    if run_after:
        subprocess.run(["uvicorn", "app.main:app", "--reload"])

