-- Schema de la base SQLite pour application Python CollectArt

DROP TABLE IF EXISTS `collection`;
CREATE TABLE IF NOT EXISTS`collection` (
	`collection_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,         
	`collection_name` TEXT NOT NULL,                                     
	`collection_collector_name` TINYTEXT NOT NULL,                      
	`collection_collector_firstname` TINYTEXT,                           
	`collection_collector_date` TINYTEXT,                                
	`collection_collector_bio` TEXT       
);

DROP TABLE IF EXISTS `mediums`;
CREATE TABLE IF NOT EXISTS `mediums` (
	`label` TEXT NOT NULL PRIMARY KEY                                       
); 

DROP TABLE IF EXISTS `work`;
CREATE TABLE IF NOT EXISTS `work` (
	`work_id` INTEGER NOT NULL PRIMARY KEY,                            
	`work_title` TINYTEXT NOT NULL,                                     
	`work_author` TEXT NOT NULL,                                        
	`work_date` INTEGER,                                                 
	`work_medium` TEXT NOT NULL,               
	`work_dimensions` TINYTEXT,                                        
	`work_image_lien` TEXT,                                           
	`work_collection_id` INTEGER NOT NULL,
	FOREIGN KEY(work_medium) REFERENCES mediums(label),
	FOREIGN KEY(work_collection_id) REFERENCES collection(collection_id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
	`user_id` INTEGER NOT NULL PRIMARY KEY,                              
	`user_name` TINYTEXT NOT NULL,                                       
	`user_login` VARCHAR ( 45 ) NOT NULL,                               
	`user_email` TINYTEXT NOT NULL,                                      
	`user_password` VARCHAR ( 100 ) NOT NULL                             
);

DROP TABLE IF EXISTS `authorship_collection`;
CREATE TABLE IF NOT EXISTS `authorship_collection` (
	`authorship_collection_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`authorship_collection_user_id` INTEGER NOT NULL,
	`authorship_collection_collection_id` INTEGER NOT NULL,
	FOREIGN KEY(authorship_collection_user_id) REFERENCES user(user_id),
	FOREIGN KEY(authorship_collection_collection_id) REFERENCES collection(collection_id)
);

 DROP TABLE IF EXISTS `authorship_work`;
CREATE TABLE IF NOT EXISTS `authorship_work` (
	`authorship_work_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`authorship_work_user_id` INTEGER NOT NULL,
	`authorship_work_work_id` INTEGER NOT NULL,
	FOREIGN KEY(authorship_work_user_id) REFERENCES user(user_id),
	FOREIGN KEY(authorship_work_work_id) REFERENCES work(work_id)
);       
