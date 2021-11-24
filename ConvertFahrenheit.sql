IF EXISTS (SELECT name
FROM sysobjects
WHERE name = 'ConvertFahrenheit'
AND type = 'TR')
DROP TRIGGER ConvertFahrenheit
GO
CREATE TRIGGER ConvertFahrenheit on MEASUREMENT_DATA
FOR update, INSERT

AS

DECLARE
@MeasurementId int,
@MeasurementValue float,
@FahrenheitValue float

select @MeasurementId = MeasurementId from INSERTED
select @MeasurementValue = MeasurementValue from INSERTED

set @FahrenheitValue = (@MeasurementValue *9)/5 + 32;
update MEASUREMENT_DATA set FahrenheitValue = @FahrenheitValue where MeasurementId = @MeasurementId

GO