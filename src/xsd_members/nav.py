from xSACdb.roles.functions import *

NAV = (
    {
        'title': 'Personal',
        'access': is_all,
        'items': [
            ('Your Profile', None, 'fa fa-user', 'xsd_members:my-profile', ['xsd_member:MyProfileEdit']),
        ]
    },
    {
        'title': 'Membership',
        'access': is_members,
        'items': [
            ('Search', None, 'fa fa-search', 'xsd_members:MemberSearch', []),
            ('Current Members', 'member', 'fa fa-th-list', 'xsd_members:MemberList', []), #['xsd_members:MemberDetail',
                                                                                      # 'xsd_members:MemberEdit',
                                                                                      # 'xsd_members:MemberDelete',
                                                                                      # 'xsd_members:MemberArchive']),
            ('Archived Members', None, 'fa fa-archive', 'xsd_members:MembersArchivedList', []),
        ]
    },
    {
        'title': 'Records Needing Attention',
        'access': is_members,
        'items': [
            ('New Members', None, 'fa fa-flag', 'xsd_members:NewMembers', []),
            ('Update Requests', None, 'fa fa-envelope-o', 'xsd_members:MemberUpdateRequestList', []),
            ('Members With Blank Fields', None, 'fa fa-ban', 'xsd_members:MembersMissingFieldsList', []),
            ('Members With Expired Forms', None, 'fa fa-exclamation-triangle', 'xsd_members:MembersExpiredFormsList', []),
        ]
    },
    {
        'title': 'Bulk Jobs',
        'access': is_members,
        'items': [
            ('Add Forms', None, 'fa fa-plus', 'xsd_members:BulkAddForms', []),
        ]
    },
    {
        'title': 'Reporting',
        'access': is_members,
        'items': [
            ('Membership Overview', None, 'fa fa-bar-chart-o', 'xsd_members:ReportsOverview', []),
        ]
    },
)
