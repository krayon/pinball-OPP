#ifndef PLAYER_H
#define PLAYER_H

#include <QString>
#include <vector>
#include <QVariant>

class Player
{
    public:
        struct PlayerInfo
        {
            int uid;
            QString lastName;
            QString firstName;
            QString email;
            QString phoneNum;
        };

        Player();
        static void read();
        static void write();
        static int numColumns();
        static int numRows();
        static QVariant cell(int row, int column);
        static void updCell(int row, int column, QString data);
        static bool addPlayer(QString lastName, QString firstName, QString phoneNum,
            QString email);

        static bool changesMade;

        static const int _UID_IDX = 0;
        static const int _LAST_NAME_IDX = 1;
        static const int _FIRST_NAME_IDX = 2;
        static const int _EMAIL_IDX = 3;
        static const int _PHONE_NUM_IDX = 4;
        static const int _NUM_COLUMNS = 5;

    private:
        static const QString _plyrFileName;
        static int _maxUid;

        static std::vector<Player::PlayerInfo> _plyrVect;
};

#endif // PLAYER_H
