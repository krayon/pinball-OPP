#include "groups.h"
#include "season.h"
#include "player.h"
#include "meet.h"

#include "logfile.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>
#include <iomanip>
#include <algorithm>

QString Groups::_groupFileName;
std::vector<Groups::GroupInfo> Groups::_groupVect;
int Groups::_num3PlyrGrps;
bool Groups::_changesMade = false;
std::vector<Groups::ChooseGrpData> Groups::_chooseGrpData;

Groups::Groups()
{

}

std::vector<Groups::GroupInfo> Groups::read()
{
    int maxUid = 0;
    int currGroupUid = 0;

    write();
    _groupFileName = QString("group.%1.txt").arg(Season::currSeason, 3, 10, QChar('0'));
    _groupVect.clear();

    QFile file(_groupFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        // Not being able to open a group file is normal if no meetings occured yet
        return (_groupVect);
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;
        std::vector<std::string> bfVect;
        GroupData tmpGrpData;
        GroupInfo tmpGrpInfo;
        std::stringstream bfStrStream;
        int meetUid;
        int groupUid;

        while(std::getline(lineStrStream, field, '$'))
        {
           fieldVect.push_back(field);
        }

        // If no fields, just ignore this line
        if (fieldVect.size() == 0)
        {
            break;
        }

        // Check if there are enough fields
        if (fieldVect.size() != _NUM_COLUMNS)
        {
            QString errorStr("Group file line does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File Field error", errorStr);
            exit(-1);
        }

        int retCode;
        int tmpVal;

        retCode = sscanf(fieldVect[_MEET_UID_IDX].c_str(), "%d", &meetUid);
        if (retCode != 1)
        {
            QString errorStr("Could not convert meet unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File meet UID convert error", errorStr);
            exit(-1);
        }
        if (meetUid == maxUid)
        {
            maxUid++;
            tmpGrpInfo.meetUid = meetUid ;
            tmpGrpInfo.grpData.clear();
            _groupVect.push_back(tmpGrpInfo);
            currGroupUid = 0;
        }
        else if (meetUid != maxUid - 1)
        {
            QString errorStr("Group file line meet UIDs must monotonically increase!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File meet UID error", errorStr);
            exit(-1);
        }

        // Convert the group UID
        retCode = sscanf(fieldVect[_GRP_UID_IDX].c_str(), "%d", &groupUid);
        if (retCode != 1)
        {
            QString errorStr("Could not convert group unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File group UID convert error", errorStr);
            exit(-1);
        }
        (void)sscanf(fieldVect[_GRP_UID_IDX].c_str(), "%d", &groupUid);
        if (groupUid == currGroupUid)
        {
            currGroupUid++;
            tmpGrpData.groupUid = groupUid;
            tmpGrpData.playerBF.clear();
            _groupVect[meetUid].grpData.push_back(tmpGrpData);
        }
        else
        {
            QString errorStr("Group file line group UIDs must monotonically increase!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File group UID error", errorStr);
            exit(-1);
        }

        bfVect.clear();
        bfStrStream.str(fieldVect[_PLAYER_BF_IDX]);
        while (std::getline(bfStrStream, field, ','))
        {
           bfVect.push_back(field);
        }

        for(auto const& value: bfVect)
        {
            retCode = sscanf(value.c_str(), "0x%x", &tmpVal);
            if (retCode != 1)
            {
                QString errorStr("Could not convert player bitfield!  " + line);

                LogFile::write(errorStr);
                QMessageBox::critical(nullptr, "Group File player bitfield convert error", errorStr);
                exit(-1);
            }
            _groupVect[meetUid].grpData[groupUid].playerBF.push_back(tmpVal);
        }
    }
    file.close();
    return (_groupVect);
}

void Groups::write()
{
    if (_changesMade)
    {
        QFile file(_groupFileName);

        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
        {
            QString errorStr("Group file could not be opened for writing.");

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Group File", errorStr);
            return;
        }

        QTextStream outTxtStream(&file);
        for (auto &meetIter : _groupVect)
        {
            for (auto &groupIter : meetIter.grpData)
            {
                outTxtStream << meetIter.meetUid << "$" << groupIter.groupUid << "$";
                for (unsigned int index = 0; index < groupIter.playerBF.size(); index++)
                {
                    if (index != 0)
                    {
                        outTxtStream << ",";
                    }
                    outTxtStream << QString("0x%1").arg(groupIter.playerBF[index], 8, 16, QChar('0'));
                }
                outTxtStream << "$" << endl;
            }
        }
        file.close();
    }
}

void Groups::createGroups(const std::vector<int>& presPlyrVect)
{
    int plyrIndex;
    int plyrBitMask;
    int oppIndex;
    int oppBitMask;
    std::vector<ChooseGrpData> chooseGrpVect;
    std::vector<SortableScoreData> sortScoreVect;
    std::vector<unsigned int> allPlyrsMask;

    // Calculate number of needed BF entries in player group masks
    int numBFEntries = ((Player::getNumPlyrs() + 0x1f) >> 5);

    allPlyrsMask.assign(numBFEntries, 0);

    for (unsigned int currIndex = 0; currIndex < presPlyrVect.size(); currIndex++)
    {
        auto currPlyrIter = presPlyrVect[currIndex];
        std::vector<int> matchVect;

        ChooseGrpData tmpGrpData;
        SortableScoreData tmpSortData;

        plyrIndex = currPlyrIter >> 5;
        plyrBitMask = 1 << (currPlyrIter & 0x1f);
        allPlyrsMask[plyrIndex] |= plyrBitMask;

        tmpGrpData.playerUid = currPlyrIter;
        tmpGrpData.nxtPossBF.assign(numBFEntries, 0);
        tmpSortData.chooseGrpIdx = currIndex;
        tmpSortData.playerUid = currPlyrIter;

        for (auto &oppIter : presPlyrVect)
        {
            if (currPlyrIter == oppIter)
            {
                // You can't play with yourself so mark as max value
                int value = _MAX_MEETS;
                matchVect.push_back(value);
            }
            else
            {
                int count = 0;
                int maxIndex;

                oppIndex = oppIter >> 5;
                oppBitMask = 1 << (oppIter & 0x1f);
                if (plyrIndex >= oppIndex)
                {
                    maxIndex = plyrIndex;
                }
                else
                {
                    maxIndex = oppIndex;
                }

                // Walk through all meets seeing if these players played together
                for (auto &meetIter : _groupVect)
                {
                    // Walk through the groups
                    for (auto &groupIter : meetIter.grpData)
                    {
                        // Make sure the bitfield exists (can happen if players added
                        // during the season)
                        if ((unsigned)maxIndex >= groupIter.playerBF.size())
                        {
                            // If the first group bit field doesn't contain enough
                            // bits, the same will be true for all groups in this meet
                            // so skip rest of meet groups
                            break;
                        }

                        // Check if the players have played together
                        if (((groupIter.playerBF[plyrIndex] & plyrBitMask) != 0) &&
                            ((groupIter.playerBF[oppIndex] & oppBitMask) != 0))
                        {
                            // Once players have played, they can't play again in same meet
                            count++;
                            break;
                        }
                        if (((groupIter.playerBF[plyrIndex] & plyrBitMask) != 0) ||
                            ((groupIter.playerBF[oppIndex] & oppBitMask) != 0))
                        {
                            // One of the players have played in the group, so that means
                            // they couldn't have played together in the meet
                            break;
                        }
                    }
                }
                matchVect.push_back(count);
            }
        }

        // Now have a filled out match vector showing number of times player played others
        // Find minimum number of matches
        int minMatches = _MAX_MEETS;
        for (auto &matchIter: matchVect)
        {
            if (matchIter < minMatches)
            {
                minMatches = matchIter;
            }
        }

        // Count number of instances of minMatches, and filll out possible match vector
        tmpGrpData.score = 0;
        for (unsigned int index = 0; index < presPlyrVect.size(); index++)
        {
            if (matchVect[index] == minMatches)
            {
                if (minMatches != 0)
                {
                    tmpGrpData.score++;
                }
                oppIndex = presPlyrVect[index] >> 5;
                oppBitMask = 1 << (presPlyrVect[index] & 0x1f);
                tmpGrpData.nxtPossBF[oppIndex] |= oppBitMask;
            }
        }
        tmpGrpData.score += (minMatches * (presPlyrVect.size() - 1));
        tmpSortData.score = tmpGrpData.score;
        chooseGrpVect.push_back(tmpGrpData);
        sortScoreVect.push_back(tmpSortData);
    }

    // Now sort the sortScoreVect by score
    std::sort(sortScoreVect.begin(), sortScoreVect.end());

    // Calculate number of players per game
    std::vector<int> plyrsInGrp;
    if (presPlyrVect.size() < 6)
    {
        plyrsInGrp.push_back(presPlyrVect.size());
    }
    else
    {
        _num3PlyrGrps = (4 - (presPlyrVect.size() % 4)) & 0x03;
        int num4PlyrGames = (presPlyrVect.size() - (_num3PlyrGrps * 3))/4;

        plyrsInGrp.assign(num4PlyrGames, 4);
        for (int index = 0; index < _num3PlyrGrps; index++)
        {
            plyrsInGrp.push_back(3);
        }
    }

    // start creating games
    std::vector<std::vector<unsigned int>> gameVect;

    for (auto &numPlyrs: plyrsInGrp)
    {
        std::vector<unsigned int> currGameBF;
        std::vector<unsigned int> possOppBF;

        currGameBF.assign(numBFEntries, 0);
        possOppBF.assign(numBFEntries, 0);

        // Find number of players with same minimal score
        int minScore = sortScoreVect[0].score;
        int numMin = 0;
        int seedPlyrIndex;
        int possOppCnt;
        int gameCurrNumPlyrs = 0;
        for (auto &chooseIter : sortScoreVect)
        {
            if (chooseIter.score == minScore)
            {
                numMin++;
            }
            else
            {
                break;
            }
        }

        // Choose seed player from players with same lowest score
        int sortIndex = rand() % numMin;
        seedPlyrIndex = sortScoreVect[sortIndex].chooseGrpIdx;

        // Add the player UID bit to the mask
        plyrIndex = chooseGrpVect[seedPlyrIndex].playerUid >> 5;
        plyrBitMask = 1 << (chooseGrpVect[seedPlyrIndex].playerUid & 0x1f);
        currGameBF[plyrIndex] |= plyrBitMask;
        gameCurrNumPlyrs++;

        // remove from allPlyrsMask and sortScoreVect since player is used
        allPlyrsMask[plyrIndex] &= ~plyrBitMask;
        sortScoreVect.erase(sortScoreVect.begin() + sortIndex);

        // initialize possOppBF
        possOppBF = allPlyrsMask;

        while (gameCurrNumPlyrs < numPlyrs)
        {
            // Find all possible best match opponents
            for (int index = 0; index < numBFEntries; index++)
            {
                possOppBF[index] &= chooseGrpVect[seedPlyrIndex].nxtPossBF[index];
            }

            int nxtPlyrIndex;
            int plyrUid;

            // See if any unmatched opponents are still available
            possOppCnt = countBits(possOppBF);
            if (possOppCnt == 0)
            {
                // No unmatched opponents available so choose from attending pool
                possOppCnt = countBits(allPlyrsMask);
                nxtPlyrIndex = rand() % possOppCnt + 1;
                plyrUid = findBit(allPlyrsMask, nxtPlyrIndex);
            }
            else
            {
                // Unmatched opponents are available
                nxtPlyrIndex = rand() % possOppCnt + 1;
                plyrUid = findBit(possOppBF, nxtPlyrIndex);
            }

            // Add the player UID bit to the mask
            plyrIndex = plyrUid >> 5;
            plyrBitMask = 1 << (plyrUid & 0x1f);
            currGameBF[plyrIndex] |= plyrBitMask;
            gameCurrNumPlyrs++;

            // remove from allPlyrsMask and sortScoreVect since player is used
            allPlyrsMask[plyrIndex] &= ~plyrBitMask;
            sortScoreVect.erase(std::find_if(sortScoreVect.begin(), sortScoreVect.end(),
                [&plyrUid](const SortableScoreData& m) -> bool { return m.playerUid == plyrUid; }));

            // Find the next index
            for (unsigned int index = 0; index < chooseGrpVect.size(); index++)
            {
                if (plyrUid == chooseGrpVect[index].playerUid)
                {
                    seedPlyrIndex = index;
                    break;
                }
            }
        }
        gameVect.push_back(currGameBF);
    }

    // Add result to the group vector
    GroupInfo tmpGrpInfo;

    tmpGrpInfo.meetUid = Meet::newMeet;
    tmpGrpInfo.grpData.clear();
    int groupUid = 0;
    for (auto &gameVectIter: gameVect)
    {
        GroupData tmpGrpData;

        tmpGrpData.groupUid = groupUid++;
        tmpGrpData.playerBF = gameVectIter;
        tmpGrpInfo.grpData.push_back(tmpGrpData);
    }
    _groupVect.push_back(tmpGrpInfo);
    _changesMade = true;
}

void Groups::addLatePlyr(const std::vector<int>& latePlyrVect)
{
    int plyrIndex;
    int plyrBitMask;
    int nxtPlyrIndex;

    // Randomly place late player into 3 person group
    for (auto &plyrIter: latePlyrVect)
    {
        plyrIndex = plyrIter >> 5;
        plyrBitMask = 1 << (plyrIter & 0x1f);
        nxtPlyrIndex = (rand() % _num3PlyrGrps) + 1;

        // Check from end of list looking for a 3 person group
        int groupMatch = 0;
        for (int index = _groupVect[Meet::newMeet].grpData.size() - 1; index >= 0; index--)
        {
            if (countBits(_groupVect[Meet::newMeet].grpData[index].playerBF) == 3)
            {
                groupMatch++;
                if (groupMatch == nxtPlyrIndex)
                {
                    // Add the late player to this group
                    _groupVect[Meet::newMeet].grpData[index].playerBF[plyrIndex] |= plyrBitMask;
                    _num3PlyrGrps--;
                    break;
                }
            }
        }
    }
}

void Groups::clearLastGroups()
{
    _groupVect.erase(_groupVect.begin() + Meet::newMeet);
}

int Groups::countBits(const std::vector<unsigned int>& data)
{
    int numBits = 0;
    unsigned int currData;

    for (auto &dataIter: data)
    {
        currData = dataIter;
        while (currData != 0)
        {
            currData &= (currData - 1);
            numBits++;
        }
    }
    return (numBits);
}

int Groups::findBit(const std::vector<unsigned int>& data, int bitInstance)
{
    unsigned int currBit = 1;
    int currCnt = 0;
    int bitOffset = 0;

    for (unsigned int index = 0; index < data.size(); index++)
    {
        currBit = 1;
        bitOffset = 0;

        while ((currBit <= data[index]) && (currBit != 0))
        {
            if ((currBit & data[index]) != 0)
            {
                currCnt++;
                if (currCnt == bitInstance)
                {
                    return (bitOffset + index);
                }
            }
            currBit <<= 1;
            bitOffset++;
        }
    }

    // Software failure:  A bit should always be found!
    QString errorStr("Software failure:  Groups::findBit could not find bit!");
    LogFile::write(errorStr);
    QMessageBox::critical(nullptr, "Group File Field error", errorStr);
    exit(-1);
}
