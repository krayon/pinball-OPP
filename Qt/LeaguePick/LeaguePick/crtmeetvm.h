#ifndef CRTMEETVM_H
#define CRTMEETVM_H

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
        std::vector<int> getPresentPlyrVect();
        std::vector<int> getLatePlyrVect();
        void clearGroups();

    private:
        struct CrtMeetInfo
        {
            int playerUid;
            bool present;
            bool disabled;
        };

        static const QStringList _labelList;
        static std::vector<CrtMeetInfo> _crtMeetVect;
        static int _currSeason;
        static int _state;
        static int _addedPlyrs;

        static const int _LAST_NAME_IDX = 0;
        static const int _FIRST_NAME_IDX = 1;
        static const int _PRESENT_IDX = 2;
        static const int _NUM_COLUMNS = 3;

        static const int _STATE_NO_GRPS = 0;
        static const int _STATE_GRPS_CREATED = 1;

        static const int _ILLEGAL_MEET = 1000;
};

#endif // CRTMEETVM_H
