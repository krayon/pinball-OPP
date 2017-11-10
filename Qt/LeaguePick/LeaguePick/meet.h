#ifndef MEET_H
#define MEET_H

#include <QString>
#include <vector>

class Meet
{
    public:
        struct MeetInfo
        {
            int uid;
            QString meetName;
        };

        Meet();
        static std::vector<Meet::MeetInfo> read();
        static void write();
        static bool addMeet(QString meetName);
        static int getUID(QString meetName);
        static void removeLastMeet();

        static int currMeet;
        static int newMeet;

        static const int _UID_IDX = 0;
        static const int _MEET_NAME_IDX = 1;
        static const int _NUM_COLUMNS = 2;

    private:
        static QString _meetFileName;
        static int _numMeets;
        static bool _changesMade;

        static std::vector<Meet::MeetInfo> _meetVect;
};

#endif // MEET_H
