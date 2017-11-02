#ifndef SEASON_H
#define SEASON_H

#include <QString>
#include <vector>

class Season
{
    public:
        struct SeasonInfo
        {
            int uid;
            QString seasonName;
            std::vector<int> playerBF;      // Player bitfield
            std::vector<int> paidBF;        // Paid bitfield
        };

        Season();
        static std::vector<Season::SeasonInfo> read();
        static void write();
        static bool addSeason(QString seasonName);
        static int getUID(QString seasonName);
        static void updateName(int seasonUid, QString seasonName);
        static bool isActPlyr(int seasonUid, int plyrUid);
        static bool isPaid(int seasonUid, int plyrUid);
        static void setActPlyr(int seasonUid, int plyrUid, bool flag);
        static void setPaid(int seasonUid, int plyrUid, bool flag);
        static void addPlyr();
        static std::vector<int> getActPlyrLst();

        static int currSeason;

        static const int _UID_IDX = 0;
        static const int _SEASON_NAME_IDX = 1;
        static const int _PLAYER_BF_IDX = 2;
        static const int _PAID_BF_IDX = 3;
        static const int _NUM_COLUMNS = 4;

    private:
        static const QString _seasonFileName;
        static bool _changesMade;
        static int _maxUid;

        static std::vector<Season::SeasonInfo> _seasonVect;
};


#endif // SEASON_H
