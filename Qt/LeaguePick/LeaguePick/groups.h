#ifndef GROUPS_H
#define GROUPS_H

#include <QString>
#include <vector>

class Groups
{
    public:
        struct GroupData
        {
            int groupUid;
            std::vector<unsigned int> playerBF;      // Player bitfield
        };

        struct GroupInfo
        {
            int meetUid;
            std::vector<GroupData> grpData;
        };

        Groups();
        static std::vector<Groups::GroupInfo> read();
        static void write();
        static void createGroups(const std::vector<int>& presPlyrVect);
        static void addLatePlyr(const std::vector<int>& latePlyrVect);
        static void clearLastGroups();

        static const int _MEET_UID_IDX = 0;
        static const int _GRP_UID_IDX = 1;
        static const int _PLAYER_BF_IDX = 2;
        static const int _NUM_COLUMNS = 3;

        static std::vector<Groups::GroupInfo> _groupVect;
        static int _num3PlyrGrps;

    private:
        struct ChooseGrpData
        {
            int playerUid;
            int score;
            std::vector<int> nxtPossBF;      // Next possible players
        };

        struct SortableScoreData
        {
            int score;
            int chooseGrpIdx;
            int playerUid;

            bool operator < (const SortableScoreData& str) const
            {
                return (score < str.score);
            }
        };

        static QString _groupFileName;
        static bool _changesMade;

        static std::vector<ChooseGrpData> _chooseGrpData;

        static int countBits(const std::vector<unsigned int>& data);
        static int findBit(const std::vector<unsigned int>& data, int bitInstance);

        static const int _MAX_MEETS = 1000;
};

#endif // GROUPS_H
