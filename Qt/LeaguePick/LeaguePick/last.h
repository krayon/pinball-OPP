#ifndef LAST_H
#define LAST_H

#include <QString>

class Last
{
    public:
        Last();
        static void read(int& season, int& meet);
        static void write();

        static const int _SEASON_IDX = 0;
        static const int _MEET_IDX = 1;
        static const int _NUM_COLUMNS = 2;

    private:
        const static QString _lastFileName;
};

#endif // LAST_H
