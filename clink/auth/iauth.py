'''
SYNOPSIS

    interface IAuth

DESCRIPTION

    Authentication, authorization base on OAuth2. Manage account.
    Use MongoDB as database.

    It uses a document named 'account' and 'group' in database, so rest parts
    of application MUST NOT uses this document name to avoid risk
    security, wrong data or causes system errors. Let use IAuth interface
    instead of read/write directly to 'account', 'group' documents.

    Document named 'account' includes fields below:

        _id [ObjectID] [required] [unique] [read-only]

            Identity of account.

        name [str] [required] [unique] [read-only]
        ^[a-z0-9-]{3,32}$

            Identity of account in human readable. It uses '-' character
            as divider. For example 'kevin-leptons'.

        hashpwd [str]

            Hash string of password, this option for implementation
            because this information is private.

            With account uses external login with other OAuth2 service such
            as google or facebook, this field is ignores and set to None.

        email [str] [required] [read-only]
        ^[a-zA-Z0-9-._]{1,64}\@
        [a-zA-Z0-9\[]{1}[a-zA-Z0-9.-:]{1,61}[a-zA-Z0-9\]]{1}$

            Follow email formatting RFC5322 section 3.2.3 and 3.4.1,
            RFC5321, RFC3696, RFC6531, RFC6523.

            However, this specification uses more strict and simple format.
            Local-part only allows three special characters'-', '.', '_'
            for readable.

            For example 'kevin.leptons@gmail.com'.

        phone [str] [read-only]
        ^\+[0-9]{2}\s[0-9]{3}\s([0-9]{3}|[0-9]{4})\s[0-9]{4}$

            This is phone number in international format. For example
            '+84 094 333 4444' or '+84 094 4444 4444'

        groups [list<str>] [required]
        ^[a-z]{2,16}$

            Groups which users belongs. It's required but can be empty list.

        created_date [unix time] [required] [read-only]

            Date when account was created.

        modified_date [unix time] [required]

            Date when account was modified. On creation time, this value
            set to created_date.
            
            On each changing of account information, this value must be
            update to time when changing was performs.

        last_action [str] [required]
            
            Last action. It must follow values

            REGISTERED: Account has been registered
            CHANGE_PWD: Password was changed
            RESET_PWD: Password was reset
            ADD_TO_GRP: Account was added to group
            RM_FRM_GRP: Account was removed from group

    Document named 'group' contains fields below:

        _id: [ObjectId] [required]

            Identity of group, it isn't used. It's exist because MongoDB
            auto creates it.

        name: [str] [required]
        ^[a-z0-9-]{2,16}$

            Name of group.

REFERENCES

    OAuth2
        https://oauth.net/2/
'''

from abc import ABC, abstractmethod


class IAuth(ABC):

    @abstractmethod
    def __init__(
        self, dbnode, root_pwd, root_email,
        jwt_key, token_time, rtoken_time
    ):
        pass

    @property
    @abstractmethod
    def accmgr(self):
        pass

    @property
    @abstractmethod
    def auth(self):
        pass
