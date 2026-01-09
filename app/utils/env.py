import os
from dotenv import load_dotenv

load_dotenv(override=False)

TRUE_VALUES = {"1", "true", "yes", "on"}
FALSE_VALUES = {"0", "false", "no", "off"}

def _require(key: str) -> str:
   value = os.getenv(key)
   if value is None:
      raise RuntimeError(f"Missing required environment variable: {key}")
   return value

def envs(key: str, default: str | None = None) -> str | None:
   return os.getenv(key, default)

def envi(key: str) -> int:
   try:
      return int(_require(key))
   except ValueError:
      raise RuntimeError(f"Invalid int value for env var: {key}")

def envf(key: str) -> float:
   try:
      return float(_require(key))
   except ValueError:
      raise RuntimeError(f"Invalid float value for env var: {key}")

def envb(key: str, default: bool | None = None) -> bool | None:
   value = os.getenv(key)

   if value is None:
      if default is not None:
         return default
      raise RuntimeError(f"Missing required boolean env var: {key}")

   value = value.lower()

   if value in TRUE_VALUES:
      return True

   if value in FALSE_VALUES:
      return False

   raise RuntimeError(f"Invalid boolean value for env var: {key}")

