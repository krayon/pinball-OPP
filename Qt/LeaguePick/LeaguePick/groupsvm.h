#ifndef GROUPSVM_H
#define GROUPSVM_H


#include <QAbstractTableModel>
#include <vector>

class GroupsVM : public QAbstractTableModel
{
    Q_OBJECT

    public:
        GroupsVM(QObject *parent);
        int rowCount(const QModelIndex &parent = QModelIndex()) const;
        int columnCount(const QModelIndex &parent = QModelIndex()) const;
        QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const;
        QVariant headerData(int section, Qt::Orientation orientation, int role) const;
        void updMeet();

    private:
        struct GroupVMInfo
        {
            int groupUid;
            int plyrUid;
        };

        static const QStringList _labelList;
        static std::vector<GroupVMInfo> _plyrGrpVect;

        static const int _GROUP_IDX = 0;
        static const int _LAST_NAME_IDX = 1;
        static const int _FIRST_NAME_IDX = 2;
        static const int _NUM_COLUMNS = 3;
};

#endif // GROUPSVM_H
