#include "groupsvm.h"

#include "player.h"
#include "meet.h"
#include "groups.h"

const QStringList GroupsVM::_labelList = {"Group", "Last Name", "First Name"};
std::vector<GroupsVM::GroupVMInfo> GroupsVM::_plyrGrpVect;

GroupsVM::GroupsVM(QObject *parent)
    :QAbstractTableModel(parent)
{

}

int GroupsVM::rowCount(const QModelIndex &parent) const
{
    (void)parent;

    return _plyrGrpVect.size();
}

int GroupsVM::columnCount(const QModelIndex &parent) const
{
    (void)parent;
    return GroupsVM::_NUM_COLUMNS;
}

QVariant GroupsVM::data(const QModelIndex &index, int role) const
{
    if (role == Qt::DisplayRole)
    {
        if (index.column() == _GROUP_IDX)
        {
            return _plyrGrpVect[index.row()].groupUid;
        }
        if (index.column() == _LAST_NAME_IDX)
        {
            return Player::getLastName(_plyrGrpVect[index.row()].plyrUid);
        }
        if (index.column() == _FIRST_NAME_IDX)
        {
            return Player::getFirstName(_plyrGrpVect[index.row()].plyrUid);
        }
    }
    return (QVariant());
}

QVariant GroupsVM::headerData(int section, Qt::Orientation orientation, int role) const
{
    if (role == Qt::DisplayRole)
    {
        if (orientation == Qt::Horizontal)
        {
            return (_labelList[section]);
        }
    }
    return QVariant();
}

void GroupsVM::updMeet()
{
    int offset;
    GroupVMInfo tmpInfo;

    _plyrGrpVect.clear();

    // Check if no meetings have occured
    if (Groups::_groupVect.size() == 0)
    {
        return;
    }

    // Walk through all the groups creating the player group vector
    for (auto &grpIter: Groups::_groupVect[Meet::currMeet].grpData)
    {
        offset = 0;
        tmpInfo.groupUid = grpIter.groupUid;

        for (auto &bfIter: grpIter.playerBF)
        {
            if (bfIter != 0)
            {
                for (int index = 0; index < 32; index++)
                {
                    if (((1 << index) & bfIter) != 0)
                    {
                        tmpInfo.plyrUid = offset + index;
                        _plyrGrpVect.push_back(tmpInfo);
                    }
                    if ((unsigned)(1 << index) >= bfIter)
                    {
                        break;
                    }
                }
            }
            offset += 32;
        }
    }
}
