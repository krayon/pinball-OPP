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
        static int getNumPlyrs();
        static QString getLastName(int plyrUid);
        static QString getFirstName(int plyrUid);
        static QString getEmail(int plyrUid);
        static QString getPhone(int plyrUid);
        static void setLastName(int plyrUid, QString data);
        static void setFirstName(int plyrUid, QString data);
        static void setEmail(int plyrUid, QString data);
        static void setPhone(int plyrUid, QString data);
        static bool addPlayer(QString lastName, QString firstName, QString phoneNum,
            QString email);


        static const int _UID_IDX = 0;
        static const int _LAST_NAME_IDX = 1;
        static const int _FIRST_NAME_IDX = 2;
        static const int _EMAIL_IDX = 3;
        static const int _PHONE_NUM_IDX = 4;
        static const int _NUM_COLUMNS = 5;

    private:
        static const QString _plyrFileName;
        static bool _changesMade;
        static int _numPlyrs;

        static std::vector<Player::PlayerInfo> _plyrVect;
};

#endif // PLAYER_H
