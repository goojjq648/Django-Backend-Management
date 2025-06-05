CREATE TABLE `restaurant` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`hash_value` VARCHAR(64) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`rating` FLOAT NOT NULL,
	`review_count` INT(10) NOT NULL,
	`address` VARCHAR(255) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`phone_number` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`average_spending` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`opening_hours` JSON NULL DEFAULT NULL,
	`services` JSON NULL DEFAULT NULL,
	`latitude` FLOAT NOT NULL,
	`longitude` FLOAT NOT NULL,
	`image_url` VARCHAR(500) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`google_url` VARCHAR(1000) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `hash_value` (`hash_value`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=98
;
CREATE TABLE `restaurantcategory` (
	`restaurant_id` INT(10) NOT NULL,
	`category_id` INT(10) NOT NULL,
	PRIMARY KEY (`restaurant_id`, `category_id`) USING BTREE,
	INDEX `idx_category_restaurant` (`category_id`, `restaurant_id`) USING BTREE,
	CONSTRAINT `restaurantcategory_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT `restaurantcategory_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
CREATE TABLE `restaurantfavorite` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`user_id` INT(10) NOT NULL,
	`restaurant_id` INT(10) NOT NULL,
	`created_at` DATETIME NULL DEFAULT (CURRENT_TIMESTAMP),
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `unique_favorite` (`user_id`, `restaurant_id`) USING BTREE,
	INDEX `restaurant_id` (`restaurant_id`) USING BTREE,
	CONSTRAINT `restaurantfavorite_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT `restaurantfavorite_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
CREATE TABLE `restaurantimage` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`restaurant_id` INT(10) NOT NULL,
	`image_url` VARCHAR(500) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `restaurant_id` (`restaurant_id`) USING BTREE,
	CONSTRAINT `restaurantimage_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
;
CREATE TABLE `restaurantreview` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`user_id` INT(10) NOT NULL,
	`restaurant_id` INT(10) NOT NULL,
	`rating` FLOAT NOT NULL,
	`review` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`created_at` DATETIME NULL DEFAULT (CURRENT_TIMESTAMP),
	`updated_at` DATETIME NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `unique_review` (`user_id`, `restaurant_id`) USING BTREE,
	INDEX `restaurant_id` (`restaurant_id`) USING BTREE,
	CONSTRAINT `restaurantreview_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE,
	CONSTRAINT `restaurantreview_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=5
;
CREATE TABLE `streets` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`city` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`district` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`road` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`latitude` DECIMAL(10,7) NULL DEFAULT NULL,
	`longitude` DECIMAL(10,7) NULL DEFAULT NULL,
	`created_at` TIMESTAMP NULL DEFAULT (CURRENT_TIMESTAMP),
	`updated_at` TIMESTAMP NULL DEFAULT (CURRENT_TIMESTAMP) ON UPDATE CURRENT_TIMESTAMP,
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `unique_street` (`city`, `district`, `road`) USING BTREE,
	INDEX `idx_city_district_road` (`city`, `district`, `road`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=35155
;
CREATE TABLE `user_userprofile` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`user_id` INT(10) NOT NULL,
	`google_id` VARCHAR(128) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`avatar_url` VARCHAR(2000) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`role` ENUM('user','admin','vendor') NULL DEFAULT 'user' COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `user_id` (`user_id`) USING BTREE,
	UNIQUE INDEX `google_id` (`google_id`) USING BTREE,
	CONSTRAINT `fk_userprofile_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=5
;
CREATE TABLE `businesshours` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`restaurant_id` INT(10) NOT NULL,
	`day_of_week` VARCHAR(10) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`open_time` TIME NOT NULL,
	`close_time` TIME NOT NULL,
	PRIMARY KEY (`id`) USING BTREE,
	INDEX `restaurant_id` (`restaurant_id`) USING BTREE,
	CONSTRAINT `businesshours_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`id`) ON UPDATE NO ACTION ON DELETE CASCADE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=7589
;
CREATE TABLE `category` (
	`id` INT(10) NOT NULL AUTO_INCREMENT,
	`name` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `unique_name` (`name`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
ENGINE=InnoDB
AUTO_INCREMENT=24
;
