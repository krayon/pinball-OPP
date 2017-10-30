#include "logfile.h"

#include "player.h"

#include <QFile>
#include <QTextStream>
#include <QMessageBox>

#include <string>
#include <sstream>

const QString Player::_plyrFileName = "player.txt";
std::vector<Player::PlayerInfo> Player::_plyrVect;
bool Player::changesMade = false;
int Player::_maxUid = 0;

Player::Player()
{

}

void Player::read()
{
    QFile file(_plyrFileName);

    if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
    {
        QString errorStr("Player file could not be opened for reading.");

        LogFile::write(errorStr);
        QMessageBox::warning(nullptr, "Player File", errorStr);
        return;
    }

    QTextStream in(&file);
    while (!in.atEnd())
    {
        QString line(in.readLine());
        std::stringstream lineStrStream(line.toStdString());
        std::string field;
        std::vector<std::string> fieldVect;
        PlayerInfo currPlyr;

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
            QString errorStr("Player file line does not contain enough fields!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Player File Field error", errorStr);
            exit(-1);
        }

        try
        {
            currPlyr.uid = stoi(fieldVect[_UID_IDX], nullptr);
            if (currPlyr.uid > _maxUid)
            {
                _maxUid = currPlyr.uid;
            }
        }
        catch (...)
        {
            QString errorStr("Could not convert unique ID!  " + line);

            LogFile::write(errorStr);
            QMessageBox::critical(nullptr, "Player File UID convert error", errorStr);
            exit(-1);
        }

        currPlyr.lastName = QString::fromStdString(fieldVect[_LAST_NAME_IDX]);
        currPlyr.firstName = QString::fromStdString(fieldVect[_FIRST_NAME_IDX]);
        currPlyr.email = QString::fromStdString(fieldVect[_EMAIL_IDX]);
        currPlyr.phoneNum = QString::fromStdString(fieldVect[_PHONE_NUM_IDX]);

        _plyrVect.push_back(currPlyr);

    }
    file.close();
}

void Player::write()
{
    QFile file(_plyrFileName);

    if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
    {
        QString errorStr("Player file could not be opened for writing.");

        LogFile::write(errorStr);
        QMessageBox::critical(nullptr, "Player File", errorStr);
        return;
    }

    QTextStream outTxtStream(&file);
    for (auto &iter : _plyrVect)
    {
        outTxtStream << iter.uid << "$" << iter.lastName << "$" << iter.firstName << \
                     "$" << iter.email << "$" << iter.phoneNum << "$" << endl;
    }
    file.close();
}

int Player::numColumns()
{
    return (_NUM_COLUMNS);
}

int Player::numRows()
{
    return _plyrVect.size();
}

QVariant Player::cell(int row, int column)
{
    switch(column)
    {
        case _UID_IDX: return(_plyrVect[row].uid);
        case _LAST_NAME_IDX: return(_plyrVect[row].lastName);
        case _FIRST_NAME_IDX: return(_plyrVect[row].firstName);
        case _EMAIL_IDX: return(_plyrVect[row].email);
        case _PHONE_NUM_IDX: return(_plyrVect[row].phoneNum);
    }
    return (QVariant());
}

void Player::updCell(int row, int column, QString data)
{
    switch(column)
    {
        case _LAST_NAME_IDX:
        {
            if (_plyrVect[row].lastName != data)
            {
                _plyrVect[row].lastName = data;
                changesMade = true;
            }
            break;
        }
        case _FIRST_NAME_IDX:
        {
            if (_plyrVect[row].firstName != data)
            {
                _plyrVect[row].firstName = data;
                changesMade = true;
            }
            break;
        }
        case _EMAIL_IDX:
        {
            if (_plyrVect[row].email != data)
            {
                _plyrVect[row].email = data;
                changesMade = true;
            }
            break;
        }
        case _PHONE_NUM_IDX:
        {
            if (_plyrVect[row].phoneNum != data)
            {
                _plyrVect[row].phoneNum = data;
                changesMade = true;
            }
            break;
        }
    }
}

bool Player::addPlayer(QString lastName, QString firstName, QString phoneNum,
    QString email)
{
    PlayerInfo currPlyr;

    if ((firstName == "") || (lastName == ""))
    {
        QMessageBox::warning(nullptr, "Player First/Last Name", "Player first and last name must be filled out.");
        return false;
    }

    _maxUid++;
    currPlyr.uid = _maxUid;
    currPlyr.lastName = lastName;
    currPlyr.firstName = firstName;
    currPlyr.email = email;
    currPlyr.phoneNum = phoneNum;

    _plyrVect.push_back(currPlyr);

    changesMade = true;
    return true;
}
