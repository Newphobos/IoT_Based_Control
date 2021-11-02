
CREATE TABLE CONFIGURATION
( 
	ConfigurationId      integer  NOT NULL  IDENTITY ,
	LoggingInterval      integer  NULL ,
	Unit                 varchar(30)  NULL ,
	SensorId             integer  NULL 
)
go

ALTER TABLE CONFIGURATION
	ADD PRIMARY KEY  CLUSTERED (ConfigurationId ASC)
go

CREATE TABLE MEASUREMENT_DATA
( 
	MeasurementId        integer  NOT NULL  IDENTITY ,
	TimeStamp            datetime  NULL ,
	MeasurementValue     float  NULL ,
	FahrenheitValue      float  NULL ,
	SensorId             integer  NULL 
)
go

ALTER TABLE MEASUREMENT_DATA
	ADD PRIMARY KEY  CLUSTERED (MeasurementId ASC)
go

CREATE TABLE SENSOR
( 
	SensorId             integer  NOT NULL  IDENTITY ,
	SensorName           varchar(30)  NULL ,
	SensorTypeId         integer  NULL 
)
go

ALTER TABLE SENSOR
	ADD PRIMARY KEY  CLUSTERED (SensorId ASC)
go

CREATE TABLE SENSOR_TYPE
( 
	SensorTypeId         integer  NOT NULL  IDENTITY ,
	SensorTypeName       varchar(30)  NULL 
)
go

ALTER TABLE SENSOR_TYPE
	ADD PRIMARY KEY  CLUSTERED (SensorTypeId ASC)
go


ALTER TABLE CONFIGURATION
	ADD  FOREIGN KEY (SensorId) REFERENCES SENSOR(SensorId)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go


ALTER TABLE MEASUREMENT_DATA
	ADD  FOREIGN KEY (SensorId) REFERENCES SENSOR(SensorId)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go


ALTER TABLE SENSOR
	ADD  FOREIGN KEY (SensorTypeId) REFERENCES SENSOR_TYPE(SensorTypeId)
		ON DELETE NO ACTION
		ON UPDATE NO ACTION
go
