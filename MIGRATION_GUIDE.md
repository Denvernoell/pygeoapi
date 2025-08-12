# Migration Guide: Flask to FastHTML & pandas to Polars

This document outlines the migration from Flask/Jinja2 to FastHTML and from pandas to Polars in the pygeoapi project.

## Overview of Changes

### 1. Web Framework Migration: Flask → FastHTML
- **Old**: Flask with Jinja2 templating
- **New**: FastHTML with reactive components and built-in HTMX
- **Benefits**: 
  - Better performance with reactive UI components
  - Built-in HTMX integration for dynamic updates
  - Simplified development with component-based architecture
  - Modern Python async support

### 2. Data Processing Migration: pandas → Polars
- **Old**: pandas for data manipulation
- **New**: Polars for high-performance columnar data processing
- **Benefits**:
  - Significantly faster performance (2-10x speedup)
  - Better memory efficiency
  - Lazy evaluation support
  - Native support for larger-than-memory datasets

## Implementation Status

### ✅ Completed
1. **Dependencies Updated**:
   - `requirements.txt`: Flask → python-fasthtml
   - `requirements-provider.txt`: pandas → polars
   - `requirements-dev.txt`: flask_cors → native FastHTML CORS
   - `Dockerfile`: Removed python3-pandas dependency

2. **Parquet Provider Updated**:
   - Replaced pandas usage with Polars in `pygeoapi/provider/parquet.py`
   - Added efficient arrow-to-polars conversion
   - Maintained geopandas compatibility where needed

3. **FastHTML App Created**:
   - New `pygeoapi/fasthtml_app.py` with modern route handling
   - CORS middleware integration
   - Starlette-based request/response handling

4. **Configuration Updated**:
   - Docker entrypoint now uses `pygeoapi.fasthtml_app:APP`
   - Removed Flask-specific system packages

5. **Documentation**:
   - Created comprehensive `.copilot` file with best practices
   - Updated `original_libraries.md` with new library choices

### 🚧 In Progress / Remaining Work

1. **Template System Migration**:
   - Current: Jinja2 templates in `pygeoapi/util.py`
   - Target: FastHTML reactive components
   - Status: Requires architectural redesign of templating system

2. **Complete API Route Migration**:
   - Current: Partial FastHTML routes implemented
   - Target: Full API coverage with FastHTML routing
   - Status: Basic routes implemented, need full coverage

3. **Provider System Updates**:
   - Current: Only parquet provider updated to Polars
   - Target: Update all providers that use pandas
   - Status: Need to audit and update other providers

4. **Testing Updates**:
   - Current: Tests still expect Flask behavior
   - Target: Update test suite for FastHTML
   - Status: Need comprehensive test migration

## Migration Benefits

### Performance Improvements
- **Polars**: 2-10x faster data processing compared to pandas
- **FastHTML**: Better rendering performance with reactive components
- **Memory**: More efficient memory usage with columnar data structures

### Developer Experience
- **Type Safety**: Better type checking with modern Python patterns
- **Reactivity**: Built-in reactive UI without complex JavaScript
- **Async Support**: Native async/await support for better scalability

### Maintainability
- **Fewer Dependencies**: FastHTML includes many features built-in
- **Modern Patterns**: Component-based architecture is more maintainable
- **Performance by Default**: Lazy evaluation and efficient data structures

## Best Practices

### Working with Polars
```python
# Use lazy evaluation for large datasets
df = pl.scan_parquet("large_file.parquet")
result = df.filter(pl.col("value") > 100).collect()

# Convert to pandas only when necessary for geopandas compatibility
pandas_df = polars_df.to_pandas()
gdf = gpd.GeoDataFrame(pandas_df, geometry='geom_column')
```

### Working with FastHTML
```python
# Use reactive components
@rt("/dynamic-data")
def dynamic_data():
    return Div(
        H2("Live Data"),
        Div(id="data-container", hx_get="/api/data", hx_trigger="load"),
        Script("htmx.process(document.body)")
    )
```

## Rollback Plan

If issues arise during migration:

1. **Revert Dependencies**: Change requirements back to Flask/pandas
2. **Revert Docker**: Update entrypoint back to flask_app
3. **Provider Rollback**: Restore pandas usage in providers
4. **Remove FastHTML**: Remove fasthtml_app.py and revert to flask_app.py

## Next Steps

1. Complete template system migration to FastHTML components
2. Update remaining data providers to use Polars
3. Migrate test suite to FastHTML patterns
4. Performance benchmarking to validate improvements
5. Update deployment documentation

## Resources

- [FastHTML Documentation](https://fasthtml.dev/)
- [Polars User Guide](https://pola-rs.github.io/polars/)
- [Migration Best Practices](.copilot)
