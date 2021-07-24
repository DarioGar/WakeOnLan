Project WakeOnLan {
  database_type: 'PostgreSQL'
    # WakeOnLan Database
}

// Creating tables
Table users as U {
  id int [pk, increment] // auto-increment
  full_name varchar
  username varchar
  password varchar
  role "user_role"
  created_at timestamp
}

Table bootup_log {
  username varchar [ref: > users.username]
  computer_ip varchar [ref: > computers.ip]
  booted_at timestamp [note: 'When computer was booted']
}

Table schedule_bootup {
  id int [pk] // primary key
  user_id int [ref: > users.id]
  computer_id int [ref: > computers.id]
  time timestamp [default: `now()`]
  days int[7]
  created_at varchar [note: 'When order created']
}

Table computers {
  id int [pk]
  last_person int [ref: > users.id]
  name varchar
  mac varchar
  cpu varchar
  ram integer [default: 0]
  ssd boolean [default: false]
  os os_type
  room_id int [ref: > rooms.id]
  latest_bootup timestamp [default: `now()`]
}

Table programs {
  computer_id int [ref: > computers.id]
  name varchar
  path varchar
}

Table work_group {
  id int [pk]
  user_id int [ref: > users.id]
  name varchar
  path varchar
  department varchar
}

Table rooms {
  id int [pk]
  group_id int [ref: > work_group.id]
  location varchar
  capacity int [default: 0]
  expected_use use_type
}

Enum user_role {
  admin
  project_manager
  regular
  learning
}

Enum os_type {
  windows
  linux
  macos
  other
}

Enum use_type{
  iot
  datascience
  cybersecurity
  regular
}
