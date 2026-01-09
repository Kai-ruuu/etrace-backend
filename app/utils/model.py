from sqlalchemy import func

def paginate(query, *, page: int, size: int, distinct_col) -> tuple:
    total = (
        query.order_by(None)
        .with_entities(func.count(func.distinct(distinct_col)))
        .scalar()
    )
    items = query.offset((page - 1) * size).limit(size).all()
    return total, items

def to_pymodels(models, pymodel):
    return [pymodel.model_validate(model) for model in models]