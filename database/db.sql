CREATE TYPE "user_role" AS ENUM (
  'admin',
  'project_manager',
  'regular',
  'learning'
);

CREATE TYPE "os_type" AS ENUM (
  'windows',
  'linux',
  'macos',
  'other'
);

CREATE TYPE "bootup_status" AS ENUM (
  'on',
  'unknown'
);

CREATE TYPE "use_type" AS ENUM (
  'iot',
  'datascience',
  'cybersecurity',
  'regular'
);

CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "full_name" varchar,
  "username" varchar,
  "password" varchar,
  "role" user_role,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE "bootup_log" (
  "user_id" SERIAL,
  "computer_id" int,
  "status" bootup_status,
  "booted_at" timestamp DEFAULT (now())
);

CREATE TABLE "schedule_bootup" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "computer_id" int,
  "time" timestamp DEFAULT (now()),
  "days" int[7],
  "created_at" varchar
);

CREATE TABLE "computers" (
  "id" SERIAL PRIMARY KEY,
  "last_person" int,
  "name" varchar,
  "mac" varchar,
  "cpu" varchar,
  "ram" integer DEFAULT 0,
  "ssd" boolean DEFAULT false,
  "os" os_type,
  "room_id" int,
  "latest_bootup" timestamp DEFAULT (now())
);

CREATE TABLE "programs" (
  "computer_id" int,
  "name" varchar,
  "path" varchar
);

CREATE TABLE "work_group" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "name" varchar,
  "path" varchar,
  "department" varchar
);

CREATE TABLE "rooms" (
  "id" SERIAL PRIMARY KEY,
  "group_id" int,
  "location" varchar,
  "capacity" int DEFAULT 0,
  "expected_use" use_type
);

ALTER TABLE "bootup_log" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "bootup_log" ADD FOREIGN KEY ("computer_id") REFERENCES "computers" ("id");

ALTER TABLE "schedule_bootup" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "schedule_bootup" ADD FOREIGN KEY ("computer_id") REFERENCES "computers" ("id");

ALTER TABLE "computers" ADD FOREIGN KEY ("last_person") REFERENCES "users" ("id");

ALTER TABLE "computers" ADD FOREIGN KEY ("room_id") REFERENCES "rooms" ("id");

ALTER TABLE "programs" ADD FOREIGN KEY ("computer_id") REFERENCES "computers" ("id");

ALTER TABLE "work_group" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "rooms" ADD FOREIGN KEY ("group_id") REFERENCES "work_group" ("id");

COMMENT ON COLUMN "bootup_log"."booted_at" IS 'When computer was booted';

COMMENT ON COLUMN "schedule_bootup"."created_at" IS 'When schedule was created';
