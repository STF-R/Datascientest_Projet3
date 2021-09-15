db.createUser(
        {
            user: "data_user",
            pwd: "data_pwd",
            roles: [
                {
                    role: "readWrite",
                    db: "wine"
                }
            ]
        }
);
