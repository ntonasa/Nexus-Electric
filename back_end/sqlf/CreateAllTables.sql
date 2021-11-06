CREATE TABLE ActualTotalLoad (
  Id               int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt  timestamp(6) NOT NULL, 
  EntityModifiedAt timestamp(6) NOT NULL, 
  ActionTaskID     bigint(20) NOT NULL, 
  Status           varchar(2), 
  Year             int(11) NOT NULL, 
  Month            int(11) NOT NULL, 
  Day              int(11) NOT NULL, 
  DateTime         datetime(6) NOT NULL, 
  AreaName         varchar(200), 
  UpdateTime       datetime(6) NOT NULL, 
  TotalLoadValue   decimal(24, 2) NOT NULL, 
  AreaTypeCodeId   int(11), 
  MapCodeId        int(11), 
  AreaCodeId       int(11) NOT NULL, 
  ResolutionCodeId int(11), 
  RowHash          varchar(255), 
  CONSTRAINT `PK_ActualTotalLoad ` 
    PRIMARY KEY (Id));
CREATE INDEX `IX_ActualTotalLoad _ResolutionCodeId` 
  ON ActualTotalLoad (ResolutionCodeId);
CREATE INDEX `IX_ActualTotalLoad _AreaCodeId` 
  ON ActualTotalLoad (AreaCodeId);
CREATE INDEX `IX_ActualTotalLoad _AreaTypeCodeId` 
  ON ActualTotalLoad (AreaTypeCodeId);
CREATE INDEX `IX_ActualTotalLoad _MapCodeId` 
  ON ActualTotalLoad (MapCodeId);
  
CREATE TABLE AggregatedGenerationPerType (
  Id                     int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt        timestamp(6) NOT NULL, 
  EntityModifiedAt       timestamp(6) NOT NULL, 
  ActionTaskID           bigint(20) NOT NULL, 
  Status                 varchar(2), 
  Year                   int(11) NOT NULL, 
  Month                  int(11) NOT NULL, 
  Day                    int(11) NOT NULL, 
  DateTime               datetime(6) NOT NULL, 
  AreaName               varchar(200), 
  UpdateTime             datetime(6) NOT NULL, 
  ActualGenerationOutput decimal(24, 2) NOT NULL, 
  ActualConsuption       decimal(24, 2) NOT NULL, 
  AreaTypeCodeId         int(11), 
  ProductionTypeId       int(11), 
  ResolutionCodeId       int(11), 
  MapCodeId              int(11), 
  AreaCodeId             int(11) NOT NULL, 
  RowHash                varchar(255), 
  CONSTRAINT `PK_AggregatedGenerationPerType ` 
    PRIMARY KEY (Id));
CREATE INDEX `IX_AggregatedGenerationPerType _AreaCodeId` 
  ON AggregatedGenerationPerType (AreaCodeId);
CREATE INDEX `IX_AggregatedGenerationPerType _ResolutionCodeId` 
  ON AggregatedGenerationPerType (ResolutionCodeId);
CREATE INDEX `IX_AggregatedGenerationPerType _ProductionTypeId` 
  ON AggregatedGenerationPerType (ProductionTypeId);
CREATE INDEX `IX_AggregatedGenerationPerType _MapCodeId` 
  ON AggregatedGenerationPerType (MapCodeId);
CREATE INDEX `IX_AggregatedGenerationPerType _AreaTypeCodeId` 
  ON AggregatedGenerationPerType (AreaTypeCodeId);


CREATE TABLE AllocatedEICDetail (
  Id                                    int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt                       timestamp(6) NOT NULL, 
  EntityModifiedAt                      timestamp(6) NOT NULL, 
  MRID                                  varchar(250), 
  DocStatusValue                        varchar(250), 
  AttributeInstanceComponent            varchar(250), 
  LongNames                             varchar(250), 
  DisplayNames                          varchar(250), 
  LastRequestDateAndOrTime              datetime(6) NULL, 
  DeactivateRequestDateAndOrTime        datetime(6) NULL, 
  MarketParticipantStreetAddressCountry varchar(250), 
  MarketParticipantACERCode             varchar(250), 
  MarketParticipantVATcode              varchar(250), 
  Description                           varchar(255), 
  EICParentMarketDocumentMRID           varchar(250), 
  ELCResponsibleMarketParticipantMRID   varchar(250), 
  IsDeleted                             bit(1) NOT NULL, 
  CONSTRAINT PK_AllocatedEICDetail 
    PRIMARY KEY (Id));


CREATE TABLE AreaTypeCode (
  Id               int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt  timestamp(6) NOT NULL, 
  EntityModifiedAt timestamp(6) NOT NULL, 
  AreaTypeCodeText varchar(255), 
  AreaTypeCodeNote varchar(255), 
  CONSTRAINT PK_AreaTypeCode 
    PRIMARY KEY (Id));
CREATE UNIQUE INDEX IX_AreaTypeCode_AreaTypeCodeText 
  ON AreaTypeCode (AreaTypeCodeText);
  
CREATE TABLE DayAheadTotalLoadForecast (
  Id               int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt  timestamp(6) NOT NULL, 
  EntityModifiedAt timestamp(6) NOT NULL, 
  ActionTaskID     bigint(20) NOT NULL, 
  Status           varchar(2), 
  Year             int(11) NOT NULL, 
  Month            int(11) NOT NULL, 
  Day              int(11) NOT NULL, 
  DateTime         datetime(6) NOT NULL, 
  AreaName         varchar(200), 
  UpdateTime       datetime(6) NOT NULL, 
  TotalLoadValue   decimal(24, 2) NOT NULL, 
  AreaTypeCodeId   int(11), 
  MapCodeId        int(11), 
  AreaCodeId       int(11) NOT NULL, 
  ResolutionCodeId int(11), 
  RowHash          varchar(255), 
  CONSTRAINT PK_DayAheadTotalLoadForecast 
    PRIMARY KEY (Id));
CREATE INDEX IX_DayAheadTotalLoadForecast_MapCodeId 
  ON DayAheadTotalLoadForecast (MapCodeId);
CREATE INDEX IX_DayAheadTotalLoadForecast_AreaTypeCodeId 
  ON DayAheadTotalLoadForecast (AreaTypeCodeId);
CREATE INDEX IX_DayAheadTotalLoadForecast_AreaCodeId 
  ON DayAheadTotalLoadForecast (AreaCodeId);
CREATE INDEX IX_DayAheadTotalLoadForecast_ResolutionCodeId 
  ON DayAheadTotalLoadForecast (ResolutionCodeId);


CREATE TABLE MapCode (
  Id               int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt  timestamp(6) NOT NULL, 
  EntityModifiedAt timestamp(6) NOT NULL, 
  MapCodeText      varchar(255), 
  MapCodeNote      varchar(255), 
  CONSTRAINT PK_MapCode 
    PRIMARY KEY (Id));
CREATE UNIQUE INDEX IX_MapCode_MapCodeText 
  ON MapCode (MapCodeText);


CREATE TABLE ProductionType (
  Id                 int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt    timestamp(6) NOT NULL, 
  EntityModifiedAt   timestamp(6) NOT NULL, 
  ProductionTypeText varchar(255), 
  ProductionTypeNote varchar(255), 
  CONSTRAINT PK_ProductionType 
    PRIMARY KEY (Id));
CREATE UNIQUE INDEX IX_ProductionType_ProductionTypeText 
  ON ProductionType (ProductionTypeText);

CREATE TABLE ResolutionCode (
  Id                 int(11) NOT NULL AUTO_INCREMENT, 
  EntityCreatedAt    timestamp(6) NOT NULL, 
  EntityModifiedAt   timestamp(6) NOT NULL, 
  ResolutionCodeText varchar(255), 
  ResolutionCodeNote varchar(255), 
  CONSTRAINT PK_ResolutionCode 
    PRIMARY KEY (Id));
CREATE UNIQUE INDEX IX_ResolutionCode_ResolutionCodeText 
  ON ResolutionCode (ResolutionCodeText);

ALTER TABLE `ActualTotalLoad` ADD CONSTRAINT FKActualTota167504 FOREIGN KEY (AreaCodeId) REFERENCES AllocatedEICDetail (Id);
ALTER TABLE `ActualTotalLoad` ADD CONSTRAINT `FK_ActualTotalLoad _AreaTypeCode_AreaTypeCodeId` FOREIGN KEY (AreaTypeCodeId) REFERENCES AreaTypeCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE `ActualTotalLoad` ADD CONSTRAINT `FK_ActualTotalLoad _MapCode_MapCodeId` FOREIGN KEY (MapCodeId) REFERENCES MapCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE `ActualTotalLoad` ADD CONSTRAINT `FK_ActualTotalLoad _ResolutionCode_ResolutionCodeId` FOREIGN KEY (ResolutionCodeId) REFERENCES ResolutionCode (Id) ON UPDATE No action ON DELETE No action;

ALTER TABLE `AggregatedGenerationPerType` ADD CONSTRAINT FKAggregated783487 FOREIGN KEY (AreaCodeId) REFERENCES AllocatedEICDetail (Id);
ALTER TABLE `AggregatedGenerationPerType` ADD CONSTRAINT `FK_AggregatedGenerationPerType _AreaTypeCode_AreaTypeCodeId` FOREIGN KEY (AreaTypeCodeId) REFERENCES AreaTypeCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE `AggregatedGenerationPerType` ADD CONSTRAINT `FK_AggregatedGenerationPerType _MapCode_MapCodeId` FOREIGN KEY (MapCodeId) REFERENCES MapCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE `AggregatedGenerationPerType` ADD CONSTRAINT `FK_AggregatedGenerationPerType _ProductionType_ProductionTypeId` FOREIGN KEY (ProductionTypeId) REFERENCES ProductionType (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE `AggregatedGenerationPerType` ADD CONSTRAINT `FK_AggregatedGenerationPerType _ResolutionCode_ResolutionCodeId` FOREIGN KEY (ResolutionCodeId) REFERENCES ResolutionCode (Id) ON UPDATE No action ON DELETE No action;

ALTER TABLE DayAheadTotalLoadForecast ADD CONSTRAINT FKDayAheadTo524780 FOREIGN KEY (AreaCodeId) REFERENCES AllocatedEICDetail (Id);
ALTER TABLE DayAheadTotalLoadForecast ADD CONSTRAINT FK_DayAheadTotalLoadForecast_AreaTypeCode_AreaTypeCodeId FOREIGN KEY (AreaTypeCodeId) REFERENCES AreaTypeCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE DayAheadTotalLoadForecast ADD CONSTRAINT FK_DayAheadTotalLoadForecast_MapCode_MapCodeId FOREIGN KEY (MapCodeId) REFERENCES MapCode (Id) ON UPDATE No action ON DELETE No action;
ALTER TABLE DayAheadTotalLoadForecast ADD CONSTRAINT FK_DayAheadTotalLoadForecast_ResolutionCode_ResolutionCodeId FOREIGN KEY (ResolutionCodeId) REFERENCES ResolutionCode (Id) ON UPDATE No action ON DELETE No action;