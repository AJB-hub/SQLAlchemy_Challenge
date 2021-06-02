## SQLAlchemy Flask App deployment

Using SQLAlchemy and flask, this python app that hosts weather data collected from weather stations in Hawaii.
The data is served locally and can be requested via API. All requested data is returned in JSON format. 

### Data Extraction
The data is extracted from a SQLite session of a database, and is queried for relevant information that is requested from the path selected.

### Data Options
Current Routes include:
* Precipitation Data by Date
* Weather Station Information
* Temperature Max, Min, Avg for custom date range

### Deployment
The server exists primarly as practice for constructing queries and backend manegment, as such there are no plans to deploy the server to take requests online. 

