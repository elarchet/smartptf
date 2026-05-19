## 0.3.0 (2026-05-19)

### Feat

- **page_export**: deactivate export in production mode
- **settings**: add DEBUG_MODE env

### Fix

- **models.load.EODHD**: drop support for EODHD loader due to changing api
- **models.load.Eodhd**: issue with eodhd api key not read
- correct DPT data initialization in MemorySession
- **models.DPT**: adapt __init__.py file to work without ai extra installed
- **utils.polars**: calculate_logR function

### Refactor

- **settings**: set csv files path into settings
- rename python modules to python snake_case convention
- **settings**: switch python-dotenv lib to pydantic_settings for variables environment
- resolve DepreciationWarning issues
- **tests**: rename 'test' folder to 'tests'

## 0.2.0 (2026-05-16)

### Fix

- correct ndim issue with dataframe

### Refactor

- add commitizen configuration
- add deptry as dev dependencies and remove unused dependencies
- move project code into src folder
