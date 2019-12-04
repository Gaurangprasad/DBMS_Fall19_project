DROP TABLE IF EXISTS ADULT_ARRESTS;

DROP TABLE  IF EXISTS  CITY_ZIP_MAP;
DROP TABLE  IF EXISTS  LIQUOR_AGENCY;
DROP TABLE  IF EXISTS LICENSE_TYPES;
DROP TABLE  IF EXISTS LIQUOR_LICENSE;

DROP TABLE  IF EXISTS  HEALTH_DEPT_COUNTY_MAP;
DROP TABLE  IF EXISTS FOOD_SERVICE_VIOLATIONS;
DROP TABLE  IF EXISTS  FOOD_SERVICE_OPERATOR;
DROP TABLE  IF EXISTS  FOOD_SERVICE_INSPECTIONS;

DROP TABLE  IF EXISTS UNEMPLOYMENT_BENEFICIARIES;

-- Adult Arrests By County

CREATE TABLE ADULT_ARRESTS(
  county varchar(255),
  year INT,
  drug_felony int,
  violent_felony int,
  dwi_felony int,
  other_felony int,
  drug_misdemeanor int,
  property_misdemeanor int,
  other_misdemeanor int,
  PRIMARY KEY (county, year)
);


-- Liquor Authority Quarterly List

CREATE TABLE LIQUOR_LICENSE(
  county varchar(255),
  license_serial_no int not null,
  license_type_code varchar(5) REFERENCES license_types(license_type_code),
  premise_name varchar(20),
  doing_business_as varchar(50),
  address varchar(255),
  zipcode int REFERENCES CITY_ZIP_MAP(zip),
  latitude  numeric(10,6) not null,
  longitude numeric(10,6) not null,
  issue_date date,
  effective_date date,
  expiration_date date,
  license_certificate_number varchar(50),
  PRIMARY KEY(license_serial_no)
);

CREATE TABLE CITY_ZIP_MAP(
  zip int,
  city varchar(50),
  state varchar(2),
  PRIMARY KEY(zip)  
);

CREATE TABLE LIQUOR_AGENCY(
  office_name varchar(50),
  office_number varchar(50),
  PRIMARY KEY(office_number)
);

CREATE TABLE LICENSE_TYPES(
  license_type_code varchar(5),
  license_class_code varchar(5),
  license_type_name varchar(100),
  PRIMARY KEY(license_type_code)
);

--  Food Service Establishments

CREATE TABLE FOOD_SERVICE_VIOLATIONS(
  violation_item varchar(20) not null,
  violation_description varchar(255) not null,
  PRIMARY KEY(violation_item)
);

CREATE TABLE HEALTH_DEPT_COUNTY_MAP(
  county varchar(255),
  local_health_department varchar(100) not null,
  PRIMARY KEY(county)
);


CREATE TABLE FOOD_SERVICE_OPERATOR(
    nys_health_operation_id         integer  not null,
    operation_name                 varchar(100) not null,
    latitude                       numeric(10,6) not null,
    longitude                      numeric(10,6) not null,
    facility_code                  varchar(10) not null,
    facility_address               varchar(255) not null,
    facility_municipality          varchar(100) not null,
    facility_city                  varchar(100) not null,
    facility_postal_zipcode        integer  not null,
    fs_facility_state              varchar(2) not null,
    permitted_dba                  varchar(100) not null,
    permitted_corp_name            varchar(100) not null,
    perm_operator_last_name        varchar(30),
    perm_operator_first_name       varchar(30),
    food_service_type              varchar(100) not null,
    food_service_description varchar(100) not null,
    permit_expiration_date         date  not null,
    PRIMARY KEY (nys_health_operation_id)
);


CREATE TABLE FOOD_SERVICE_INSPECTIONS(
  county varchar(255),
  date_of_inspection date not null,
  nys_health_operation_id integer not null REFERENCES FOOD_SERVICE_OPERATOR(nys_health_operation_id),
  violation_item varchar(20) not null REFERENCES FOOD_SERVICE_VIOLATIONS(violation_item),
  critical_violation varchar(100) not null,
  total_critical_violations integer not null,
  total_crit_not_corrected integer not null,
  total_noncritical_violations integer not null,
  nysdoh_gazetteer_1980 integer not null,
  inspection_type varchar(50) not null,
  inspection_comments varchar(255) not null,
  PRIMARY KEY (nys_health_operation_id, date_of_inspection)
);


-- Unemployment beneficiaries

CREATE TABLE UNEMPLOYMENT_BENEFICIARIES(
  year INT,
  month VARCHAR(255),
  region VARCHAR(255),
  county VARCHAR(255),
  beneficiaries INT,
  benefit_amt INT,
  PRIMARY KEY (year, county, month)
);

-