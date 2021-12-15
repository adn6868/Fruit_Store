/*
 Navicat Premium Data Transfer

 Source Server         : postgres
 Source Server Type    : PostgreSQL
 Source Server Version : 140000
 Source Host           : localhost:5432
 Source Catalog        : fruit_store
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 140000
 File Encoding         : 65001

 Date: 08/11/2021 11:38:45
*/


-- ----------------------------
-- Table structure for itemTbl
-- ----------------------------
DROP TABLE IF EXISTS "public"."itemTbl";
CREATE TABLE "public"."itemTbl" (
  "item_id" int4 NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."itemTbl" OWNER TO "postgres";

-- ----------------------------
-- Records of itemTbl
-- ----------------------------
BEGIN;
INSERT INTO "public"."itemTbl" VALUES (1, 'Chuoi');
INSERT INTO "public"."itemTbl" VALUES (19, 'Tao');
COMMIT;

-- ----------------------------
-- Table structure for orderTbl
-- ----------------------------
DROP TABLE IF EXISTS "public"."orderTbl";
CREATE TABLE "public"."orderTbl" (
  "order_id" int4 NOT NULL,
  "item_list" varchar(255) COLLATE "pg_catalog"."default",
  "customer" varchar(255) COLLATE "pg_catalog"."default"
)
;
ALTER TABLE "public"."orderTbl" OWNER TO "postgres";

-- ----------------------------
-- Records of orderTbl
-- ----------------------------
BEGIN;
INSERT INTO "public"."orderTbl" VALUES (11, 'Chuoi, Tao', 'Duc Anh');
INSERT INTO "public"."orderTbl" VALUES (1, 'Tao', 'Duc Anh');
COMMIT;

-- ----------------------------
-- Primary Key structure for table itemTbl
-- ----------------------------
ALTER TABLE "public"."itemTbl" ADD CONSTRAINT "itemTbl_pkey" PRIMARY KEY ("item_id");

-- ----------------------------
-- Primary Key structure for table orderTbl
-- ----------------------------
ALTER TABLE "public"."orderTbl" ADD CONSTRAINT "orderTbl_pkey" PRIMARY KEY ("order_id");
