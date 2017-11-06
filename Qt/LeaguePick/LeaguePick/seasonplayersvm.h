#ifndef SEASONPLAYERSVM_H
#define SEASONPLAYERSVM_H

#include <QAbstractTableModel>
#include <vector>

class SeasonPlayersVM : public QAbstractTableModel
{
    Q_OBJECT

    public:
        SeasonPlayersVM(QObject *parent);
        int rowCount(const QModelIndex &parent = QModelIndex()) const;
        int columnCount(const QModelIndex &parent = QModelIndex()) const;
        QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role) const;
        Qt::ItemFlags flags(const QModelIndex& index) const;
        void addRow();
        bool setData(const QModelIndex & index, const QVariant & value, int role = Qt::EditRole);

    private:
        struct SeasonPlyrInfo
        {
            bool paid;
            bool inSeason;
        };

        static const QStringList _labelList;
        static bool _hide;
        static std::vector<SeasonPlyrInfo> _seasonVect;

        static const int _LAST_NAME_IDX = 0;
        static const int _FIRST_NAME_IDX = 1;
        static const int _PAID_IDX = 2;
        static const int _IN_SEASON_IDX = 3;
        static const int _NUM_COLUMNS = 4;
};

#endif // SEASONPLAYERSVM_H
