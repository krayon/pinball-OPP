#ifndef CRTMEETVM_H
#define CRTMEETVM_H

#include "player.h"

#include <QAbstractTableModel>
#include <vector>

class CrtMeetVM : public QAbstractTableModel
{
    Q_OBJECT

    public:
        CrtMeetVM(QObject *parent);
        int rowCount(const QModelIndex &parent = QModelIndex()) const;
        int columnCount(const QModelIndex &parent = QModelIndex()) const;
        QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role) const;
        Qt::ItemFlags flags(const QModelIndex& index) const;
        void addRow();
        bool setData(const QModelIndex & index, const QVariant & value, int role = Qt::EditRole);
        void updSeasonPlyr();

    private:
        struct CrtMeetInfo
        {
            int playerUid;
            bool present;
        };

        static const QStringList _labelList;
        static std::vector<CrtMeetInfo> _crtMeetVect;
        static int _currSeason;

        static const int _LAST_NAME_IDX = 0;
        static const int _FIRST_NAME_IDX = 1;
        static const int _PRESENT_IDX = 2;
        static const int _NUM_COLUMNS = 3;

        static const int _ILLEGAL_MEET = 1000;
};

#endif // CRTMEETVM_H
