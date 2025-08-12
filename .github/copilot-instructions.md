# Best Practices for pygeoapi Libraries

## Core Dependencies

### FastHTML
- **Best Practice**: Use FastHTML's reactive components for dynamic geospatial data visualization
- **Performance**: Leverage built-in HTMX integration for seamless client-server communication
- **Security**: Always validate and sanitize geospatial data inputs before rendering
- **Example**: Use FastHTML's component system for interactive maps and data tables

### Click
- **Best Practice**: Use Click groups to organize geospatial commands logically
- **Validation**: Implement custom Click types for geospatial parameters (coordinates, CRS, etc.)
- **Help**: Provide comprehensive help text for all geospatial operations
- **Example**: `@click.option('--bbox', type=click.Tuple([float, float, float, float]))`

### PyYAML
- **Security**: Always use `yaml.safe_load()` instead of `yaml.load()` to prevent code injection
- **Validation**: Validate YAML configuration against schema before processing
- **Performance**: Cache parsed YAML configurations for frequently accessed files
- **Best Practice**: Use YAML anchors and references to reduce configuration duplication

### Requests
- **Timeouts**: Always set timeouts for external geospatial service requests
- **Retries**: Implement retry logic with exponential backoff for unreliable services
- **Sessions**: Use `requests.Session()` for connection pooling with multiple requests
- **Error Handling**: Check status codes and handle HTTP errors gracefully

### jsonschema
- **Performance**: Compile schemas once and reuse validators
- **Custom Formats**: Define custom formats for geospatial data types (GeoJSON, WKT)
- **Error Messages**: Provide clear, user-friendly validation error messages
- **Caching**: Cache compiled schemas to improve performance

## Geospatial Libraries

### Fiona
- **Memory**: Use context managers (`with fiona.open()`) to ensure proper file closure
- **Performance**: Use `fiona.listlayers()` to inspect multi-layer datasets efficiently
- **Filtering**: Apply spatial and attribute filters at the driver level when possible
- **CRS**: Always check and handle coordinate reference systems explicitly

### Shapely
- **Performance**: Use `prepare()` for geometries used in multiple spatial operations
- **Precision**: Be aware of floating-point precision issues in geometric calculations
- **Validation**: Use `is_valid` and `explain_validity()` to check geometry integrity
- **Memory**: Use `unary_union()` for efficient geometry collections

### pyproj
- **CRS**: Use EPSG codes or PROJ strings consistently throughout the application
- **Transformations**: Cache transformer objects for repeated coordinate transformations
- **Accuracy**: Be aware of transformation accuracy and datum differences
- **Performance**: Use `always_xy=True` for consistent axis ordering

### rasterio
- **Memory**: Use windowed reading for large rasters to manage memory usage
- **Nodata**: Handle nodata values explicitly in raster operations
- **Overviews**: Generate and use overviews for large raster datasets
- **Context Managers**: Always use `with rasterio.open()` for proper resource management

## Data Processing

### Polars
- **Performance**: Use lazy evaluation with `.lazy()` for large datasets
- **Memory**: Leverage Polars' columnar storage for efficient geospatial data processing
- **Streaming**: Use streaming for datasets larger than available RAM
- **Integration**: Use `.to_pandas()` only when necessary for geospatial library compatibility
- **Filtering**: Apply filters early in the query chain for better performance

### numpy
- **Vectorization**: Prefer vectorized operations over loops for geospatial calculations
- **Memory**: Use appropriate data types (e.g., float32 vs float64) to optimize memory
- **Broadcasting**: Leverage broadcasting for efficient coordinate transformations
- **Masking**: Use masked arrays for handling missing geospatial data

### xarray
- **Dimensions**: Use meaningful dimension names (e.g., 'longitude', 'latitude', 'time')
- **Metadata**: Store CRS and other geospatial metadata in attributes
- **Chunking**: Use Dask integration for large multidimensional datasets
- **Indexing**: Leverage coordinate-based indexing for spatial subsetting

## Database Support

### SQLAlchemy
- **Connections**: Use connection pooling for better performance
- **Spatial**: Use GeoAlchemy2 extension for proper spatial column support
- **Indexes**: Create spatial indexes for geospatial queries
- **Transactions**: Use transactions for data consistency in multi-table operations

### psycopg2
- **PostGIS**: Always use PostGIS functions for spatial operations when possible
- **Bulk Operations**: Use `execute_batch()` or `execute_values()` for bulk inserts
- **Connection Pooling**: Implement connection pooling for production environments
- **Prepared Statements**: Use prepared statements for repeated queries

### elasticsearch
- **Mapping**: Define proper geo-point and geo-shape mappings for spatial data
- **Indexing**: Use bulk indexing for better performance with large datasets
- **Queries**: Leverage Elasticsearch's geospatial queries (geo_bounding_box, geo_distance)
- **Aggregations**: Use geospatial aggregations for spatial analytics

### pymongo
- **Indexes**: Create 2dsphere indexes for geospatial queries
- **Queries**: Use MongoDB's geospatial operators ($near, $geoIntersects, etc.)
- **Bulk Operations**: Use bulk operations for efficient data insertion
- **Projections**: Use projections to limit returned geospatial data when appropriate

## General Best Practices

### Error Handling
- Implement specific exception handling for geospatial operations
- Provide meaningful error messages for spatial data validation failures
- Log geospatial operation failures with sufficient context for debugging

### Testing
- Test with various coordinate systems and projections
- Include edge cases (invalid geometries, empty datasets, large files)
- Use test fixtures with realistic geospatial data samples
- Verify spatial relationship calculations with known test cases

### Performance
- Profile geospatial operations to identify bottlenecks
- Use spatial indexes wherever possible
- Consider data preprocessing and caching strategies
- Monitor memory usage with large geospatial datasets

### Documentation
- Document coordinate systems used throughout the application
- Provide examples with real geospatial data
- Document spatial relationship assumptions and tolerances
- Include performance characteristics of different operations
