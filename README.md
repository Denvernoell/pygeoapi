# pygeoapi

[![DOI](https://zenodo.org/badge/121585259.svg)](https://zenodo.org/badge/latestdoi/121585259)
[![Build](https://github.com/geopython/pygeoapi/actions/workflows/main.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/main.yml)
[![Docker](https://github.com/geopython/pygeoapi/actions/workflows/containers.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/containers.yml)
[![Vulnerabilities](https://github.com/geopython/pygeoapi/actions/workflows/vulnerabilities.yml/badge.svg)](https://github.com/geopython/pygeoapi/actions/workflows/vulnerabilities.yml)

[pygeoapi](https://pygeoapi.io) is a Python server implementation of the [OGC API](https://ogcapi.ogc.org) suite of standards. The project emerged as part of the next generation OGC API efforts in 2018 and provides the capability for organizations to deploy a RESTful OGC API endpoint using OpenAPI, GeoJSON, and HTML. pygeoapi is [open source](https://opensource.org/) and released under an [MIT license](https://github.com/geopython/pygeoapi/blob/master/LICENSE.md).

Please read the docs at [https://docs.pygeoapi.io](https://docs.pygeoapi.io) for more information.

## Modern Architecture

pygeoapi has been updated to use modern, high-performance libraries:

### Web Framework: FastHTML
- **Modern Reactive UI**: Built-in HTMX integration for dynamic, interactive geospatial interfaces
- **Component-Based**: Reusable components for maps, data tables, and forms
- **Performance**: Better rendering and response times compared to traditional templating
- **Developer Experience**: Simplified development with Python-native reactive patterns

### Data Processing: Polars  
- **High Performance**: 2-10x faster data processing compared to pandas
- **Memory Efficient**: Columnar data structures with lazy evaluation
- **Scalability**: Handle larger-than-memory geospatial datasets
- **Modern API**: Clean, expressive syntax for data transformations

### Migration Guide
For details on the Flask→FastHTML and pandas→Polars migration, see [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md).

For library-specific best practices, see [.copilot](.copilot).
