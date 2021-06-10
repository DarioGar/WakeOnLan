DO $$ BEGIN
CREATE TYPE "user_role" AS ENUM (
  'admin',
  'project_manager',
  'regular',
  'learning'
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
CREATE TYPE "invitation_status" AS ENUM (
  'on hold',
  'accepted',
  'refused'
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
CREATE TYPE "os_type" AS ENUM (
  'windows',
  'linux',
  'macos',
  'other'
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
CREATE TYPE "bootup_status" AS ENUM (
  'on',
  'unknown'
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
CREATE TYPE "use_type" AS ENUM (
  'iot',
  'datascience',
  'cybersecurity',
  'regular'
);
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS "users" (
  "id" SERIAL PRIMARY KEY,
  "full_name" varchar,
  "username" varchar,
  "password" varchar,
  "role" user_role,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS "invitations" (
  "id" SERIAL PRIMARY KEY,
  "sender" int,
  "receiver" int,
  "groupId" int,
  "status" invitation_status,
  "created_at" timestamp DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS "bootup_log" (
  "user_id" SERIAL,
  "computer_id" int,
  "status" bootup_status,
  "booted_at" timestamp DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS "schedule_bootup" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "computer_id" int,
  "time" timestamp DEFAULT (now()),
  "days" varchar[7],
  "created_at" varchar DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS "computers" (
  "id" SERIAL PRIMARY KEY,
  "last_person" int,
  "name" varchar,
  "mac" varchar,
  "cpu" varchar,
  "gpu" varchar,
  "ip" varchar,
  "ram" integer DEFAULT 0,
  "ssd" boolean DEFAULT false,
  "os" os_type,
  "room_id" int,
  "latest_bootup" timestamp DEFAULT (now())
);

CREATE TABLE IF NOT EXISTS "programs" (
  "computer_id" int,
  "name" varchar,
  "path" varchar
);

CREATE TABLE IF NOT EXISTS "work_group" (
  "id" SERIAL PRIMARY KEY,
  "user_id" int,
  "name" varchar,
  "path" varchar,
  "department" varchar
);

CREATE TABLE IF NOT EXISTS "rooms" (
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

ALTER TABLE "invitations" ADD FOREIGN KEY ("sender") REFERENCES "users" ("id");

ALTER TABLE "invitations" ADD FOREIGN KEY ("receiver") REFERENCES "users" ("id");

ALTER TABLE "invitations" ADD FOREIGN KEY ("groupId") REFERENCES "work_group" ("id");

COMMENT ON COLUMN "bootup_log"."booted_at" IS 'When computer was booted';

COMMENT ON COLUMN "schedule_bootup"."created_at" IS 'When schedule was created';

ALTER TABLE "schedule_bootup" DROP CONSTRAINT IF EXISTS time_days_unique;
ALTER TABLE "schedule_bootup" ADD CONSTRAINT time_days_unique UNIQUE ("computer_id","time", "days");

ALTER TABLE "invitations" DROP CONSTRAINT IF EXISTS unique_invitation;
ALTER TABLE "invitations" ADD CONSTRAINT unique_invitation UNIQUE ("sender","receiver", "groupId");