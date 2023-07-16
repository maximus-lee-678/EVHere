 CREATE TABLE connector_type ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	name_short           VARCHAR(8) NOT NULL     ,
	name_long            VARCHAR(64) NOT NULL     ,
	name_connector       VARCHAR(64) NOT NULL
 );

CREATE TABLE charger ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	name                 VARCHAR(255) NOT NULL    ,
	latitude             DECIMAL(7) NOT NULL    ,
	longitude            DECIMAL(7) NOT NULL    ,
	address              VARCHAR(512) NOT NULL    ,
	currently_open        INT NOT NULL    ,
	pv_current_in        DECIMAL(2) NOT NULL    ,
	pv_energy_level      DECIMAL(2) NOT NULL    ,
	rate_current         DECIMAL(2) NOT NULL    ,
	rate_predicted       VARCHAR(255) NOT NULL    ,
	active               INT NOT NULL    ,
	last_updated         DATETIME NOT NULL    
 );

 CREATE TABLE charger_available_connector ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_charger           CHAR(36) NOT NULL    ,
	id_connector_type    CHAR(36) NOT NULL    ,
	in_use               INT NOT NULL    ,
	output_current       DECIMAL(2)     ,
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )  ,
	FOREIGN KEY ( id_connector_type ) REFERENCES connector_type( id )
 );

CREATE TABLE user_info ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	username             VARCHAR(64) NOT NULL    ,
	password             VARCHAR(64) NOT NULL    ,
	email                VARCHAR(255) NOT NULL    ,
	full_name            VARCHAR(255) NOT NULL    ,
	phone_no             VARCHAR(8)     ,
	created_at           DATETIME NOT NULL    ,
	modified_at          DATETIME NOT NULL    
 );

 CREATE TABLE vehicle_info (
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	name                 VARCHAR(64) NOT NULL    ,
	model                VARCHAR(64) NOT NULL    ,
	vehicle_sn           VARCHAR(8) NOT NULL    ,
	id_connector_type    CHAR(36) NOT NULL    ,
	active               INT NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_connector_type ) REFERENCES connector_type( id )
 );

CREATE TABLE favourited_chargers ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	id_charger           CHAR(36) NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )  
 );

 CREATE TABLE charge_current ( 
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_charge_history    CHAR(36) NOT NULL    ,
	id_charger_available_connector CHAR(36) NOT NULL    ,
	current_energy_drawn DECIMAL(2) NOT NULL    ,
	rate_snapshot        DECIMAL(2) NOT NULL    ,
	last_updated         DATETIME NOT NULL   ,
	FOREIGN KEY ( id_charge_history ) REFERENCES charge_history( id )  ,
	FOREIGN KEY ( id_charger_available_connector ) REFERENCES charger_available_connector( id )  
 );

CREATE TABLE charge_history (
	id                   CHAR(36) NOT NULL  PRIMARY KEY  ,
	id_user_info         CHAR(36) NOT NULL    ,
	id_vehicle_info      CHAR(36) NOT NULL    ,
	id_charger           CHAR(36) NOT NULL    ,
	time_start           DATETIME NOT NULL    ,
	time_end             DATETIME    ,
	total_energy_drawn   DECIMAL(2)     ,
	amount_payable       DECIMAL(2)     ,
	is_charge_finished   INT NOT NULL    ,
	FOREIGN KEY ( id_user_info ) REFERENCES user_info( id )  ,
	FOREIGN KEY ( id_vehicle_info ) REFERENCES vehicle_info( id )  , 
	FOREIGN KEY ( id_charger ) REFERENCES charger( id )
);