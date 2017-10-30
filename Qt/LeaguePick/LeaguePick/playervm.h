#ifndef PLAYERVM_H
#define PLAYERVM_H

#include "player.h"

#include <QAbstractTableModel>

class PlayerVM : public QAbstractTableModel
{
    Q_OBJECT

    public:
        PlayerVM(QObject *parent);
        int rowCount(const QModelIndex &parent = QModelIndex()) const;
        int columnCount(const QModelIndex &parent = QModelIndex()) const;
        QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role) const;
        Qt::ItemFlags flags(const QModelIndex& index) const;
        bool setData(const QModelIndex & index, const QVariant & value, int role = Qt::EditRole);
        void addRow();

    private:
        static const QStringList _labelList;

        static const int _UID_IDX = 0;
        static const int _LAST_NAME_IDX = 1;
        static const int _FIRST_NAME_IDX = 2;
        static const int _EMAIL_IDX = 3;
        static const int _PHONE_NUM_IDX = 4;
        static const int _NUM_COLUMNS = 5;
};

#endif // PLAYERVM_H
