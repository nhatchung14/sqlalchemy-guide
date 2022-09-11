echo "SELECT * FROM users;"
sqlite3 user.db 'SELECT * FROM users;'
echo ""

echo "SELECT * FROM emails;"
sqlite3 user.db 'SELECT * FROM emails;'
echo ""

echo "SELECT * FROM roles;"
sqlite3 user.db 'SELECT * FROM roles;'
echo ""

echo "SELECT * FROM user_roles;"
sqlite3 user.db 'SELECT * FROM user_roles;'
echo ""