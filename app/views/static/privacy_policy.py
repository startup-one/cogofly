# coding=UTF-8
# Page statique : "À propos"


from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _


class PrivacyPolicyView(View):
    template_name = 'static/privacy_policy.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'privacy_policy_title': _('Cogofly - Privacy policy'),
            'privacy_policy_data_protection':
                _('Data protection is of the utmost importance to'
                  '<strong>COGOFLY</strong> (right after '
                  '"<strong>COGOFLY</strong>"). '
                  'The Privacy Policy in place supplements the Terms and '
                  'Conditions of the website www.<strong>COGOFLY</strong>.com '
                  '(referred to hereafter as "the Website"), governing the '
                  'relationship between the user and <strong>COGOFLY</strong'
                  '>. This Privacy Policy applies to all services provided on '
                  'the Website. The French version of this Privacy Policy '
                  'shall prevail over any other version. The user can contact '
                  '<strong>COGOFLY</strong> by the following email: <strong>'
                  'COGOFLY</strong>@gmail.com. By registering on the Website, '
                  'the user consents to this Privacy Policy.'),
            'privacy_policy_1_collection':
                _('1. Collection of personal data:'),
            'privacy_policy_1_collection_details':
                _('<strong>COGOFLY</strong> collects, processes, and uses '
                  'personal data about the users in accordance with French '
                  'and Europe laws and statutes on data protection. This '
                  'collection has been declared to the CNIL under number '
                  '1822236v0. <strong>COGOFLY</strong> uses personal data in '
                  'the exclusive goal of providing the user with the services '
                  'described on the Website and in the Terms and Conditions. <'
                  'strong>COGOFLY</strong> will never transfer Personal Data '
                  'to third parties without the user\'s consent. The user has '
                  'a right of access, rectification and opposition on his/her '
                  'personal data. To exercise those rights, the user shall '
                  'contact <strong>COGOFLY</strong> by the contact email.'),
            'privacy_policy_2_registration':
                _('2. Registration:'),
            'privacy_policy_2_registration_details':
                _('In order to become a user of the Website, it is necessary '
                  'to first create an account on the Website. To create an '
                  'account, the user is required to provide the following '
                  'mandatory contact information:'),
            'privacy_policy_2_registration_details_enum': [
                _('For a "solo" account: email, password or social network '
                  'account such as Facebook, Twitter, Instagram, Pinterest, '
                  'LinkedIn, Viadeo, Google +, family name, first name, '
                  'country and city of residence, country and city of birth, '
                  'gender, date of birth, at least one place the user wishes '
                  'to visit.'),
                _('For a group account: same information as for a "solo" '
                  'account, but concerning at least two users (except for the '
                  'users who are already registered in the Website).'),
                _('For a couple account: same information as for a "solo" '
                  'account, but concerning both users of the couple (except '
                  'if the two users who are already registered in the'
                  'Website).'),
                _('For a family account: same information as for a "solo" '
                  'account, but concerning all the users of the Family ('
                  'except for the users who are already registered in the '
                  'Website).')],
            'privacy_policy_3_profile_information':
                _('3. Profile Information and contents:'),
            'privacy_policy_3_profile_information_details':
                _('Once registered, the user may provide other optional '
                  'pieces of information (profession, diplomas, languages, '
                  'hobbies, and so on...). The user can also publish or post '
                  'different contents on the Website. These pieces of '
                  'information are collected by <strong>COGOFLY</strong> to '
                  'provide the user with better services and more '
                  'confidence.'),
            'privacy_policy_4_users_contacts':
                _('4. Information about the user\'s contacts:'),
            'privacy_policy_4_users_contacts_details_1':
                _('If the user chooses to invite other people to join his '
                  'entity, he/she shall enter the last name, first name, and '
                  'email addresses of the invitees, or just their email '
                  'address and potentially a phone number, depending on the '
                  'data required by the invitation. This data is used only to '
                  'send the invitation email and other reminders. <strong>'
                  'COGOFLY</strong> stores this information to send the '
                  'invitation email and to register a contact connexion if '
                  'the user\'s invitation is accepted.'),
            'privacy_policy_4_users_contacts_details_2':
                _('All information entered or uploaded about contacts is '
                  'considered personal data for the application of this '
                  'Privacy Policy.'),
            'privacy_policy_5_cookies':
                _('5. Cookies:'),
            'privacy_policy_5_cookies_details_1':
                _('<strong>COGOFLY</strong> uses cookies to identify the user '
                  'during the course of his/her session and to recognise him/'
                  'her as a user when he/she returns to the Website using the '
                  'same computer and web browser. A cookie is a file stored '
                  'on the user\'s computer tied to information about the '
                  'user. <strong>COGOFLY</strong> uses session ID cookies to '
                  'confirm that the user is logged in. These cookies '
                  'terminate once the user closes the browser. By default, '
                  '<strong>COGOFLY</strong> uses persistent cookies that '
                  'store the user\'s login ID (but not the password) to make '
                  'it easier for the user to log in when he/she comes back to '
                  'the Website. These cookies will then store part of the '
                  'login data in encrypted form. The user can remove or block '
                  'these cookies using the settings in the browser if he/she '
                  'wants to disable this convenience feature. Unfortunately, '
                  'if the browser settings do not allow cookies, the user '
                  'shall systematically give his user name and password to '
                  'log on.'),
            'privacy_policy_5_cookies_details_2':
                _('<strong>COGOFLY</strong> also receives the IP address of '
                  'the user\'s computer, the computer operating system and '
                  'type of web browser he/she is using, as well as the name '
                  'of the user\'s ISP.'),
            'privacy_policy_5_cookies_details_3':
                _('This data is saved in a log file and will be stored by. '
                  'The information is used in anonymous form to analyse '
                  'overall trends to help <strong>COGOFLY</strong> improve '
                  'its service, e.g., <strong>COGOFLY</strong> may analyse on '
                  'which days, at which time and when the Website are '
                  'particularly frequented. The linkage between the '
                  'user\'s IP address and his/her personally identifiable '
                  'information is never shared with any third party without '
                  'the user\'s permission except when required by law. '
                  '<strong>COGOFLY</strong> reserves the right to review the '
                  'log files from the last known IP address of the user where '
                  '<strong>COGOFLY</strong> has reasonable cause to believe '
                  'that the user is using the Website in breach of the '
                  'Terms and Conditions or the applicable legislation. '
                  'In doing this, <strong>COGOFLY</strong> protects other '
                  'users, the safety of its user\'s '
                  'data, as well as the Website and the services. Like the '
                  'information the user enters at registration or in his/her '
                  'profile, cookie and associated log file data is used to '
                  'customise the use of the Website and to help the user to '
                  'not type his user name and password again. By using the '
                  'Website and/or registering with the Website, the user '
                  'fully accepts the use of the above mentioned cookies and '
                  'log files.'),
            'privacy_policy_6_viewable_datas':
                _('6. Viewable data:'),
            'privacy_policy_6_viewable_datas_1':
                _('When the user registers in the Website, he/she may choose '
                  'by whom his/her profile information are viewable. Three '
                  'choices are then available: profile Information can be '
                  'viewable either by everybody or solely by the user\'s '
                  'contacts/friends or solely by the user\'s himself/herself. '
                  'The user may modify his/her choice at any time in the '
                  'settings menu. However, the profile picture will always be '
                  'viewable by everybody. This picture will be blurred when '
                  'the profiles research succeeds, <strong>COGOFLY</strong> '
                  'wishing to be clearly different from a dating website. If '
                  'the user makes no choice when registering, the following '
                  'rules apply by default:'),
            'privacy_policy_6_viewable_datas_2':
                _('Viewable by everybody: family name, first name, country'
                  '/city of residence, country/city of birth, gender, date of '
                  'birth, scholarship/diplomas, schools/universities, former '
                  'country/city of residence, languages, current profession, '
                  'current employer, former employers, types of licences, '
                  'zodiacal sign, what the User has already visited/done, '
                  'what the user wishes to visit/do, interests, hobbies, self-'
                  'description, smoker, number of children, statute.'),
            'privacy_policy_6_viewable_datas_3':
                _('Viewable solely by the user: email address.'),
            'privacy_policy_7_sharing_information':
                _('7. Sharing information with other users of <strong>COGOFLY'
                  '</strong> or third parties:'),
            'privacy_policy_7_sharing_information_details_1':
                _('Profile information is only available to other users of <'
                  'strong>COGOFLY</strong> depending on the user\'s chosen '
                  'individual privacy settings. Neither third parties ('
                  'meaning not registered users) nor searching engines (eg : '
                  'Google, Bing, Yahoo, etc…) have access to the user\'s '
                  'profile information, contents and personal data. The user '
                  'acknowledges that no security measures are perfect and '
                  'that the user\'s personal data may become publicly '
                  'available, in case of a website hacking for example, '
                  'despite the efforts of <strong>COGOFLY</strong> '
                  'to maintain security of the Website. '
                  '<strong>COGOFLY</strong> cannot control '
                  'the actions of other users with whom the user may shares '
                  'data and information. Therefore, <strong>COGOFLY</strong> '
                  'does not guarantee that personal data will not be viewed '
                  'by unauthorised persons. <strong>COGOFLY</strong> is not '
                  'responsible for circumvention of any privacy settings or '
                  'security measures contained on the Website.'),
            'privacy_policy_7_sharing_information_details_2':
                _('The user also acknowledges that, even after removal, '
                  'copies of personal data may remain viewable in cached and '
                  'archived pages.'),
            'privacy_policy_8_emails_and_notifications':
                _('8. Emails, and Notifications to users:'),
            'privacy_policy_8_emails_and_notifications_details':
                _('<strong>COGOFLY</strong> regularly sends out notification '
                  'messages and emails to all users of '
                  '<strong>COGOFLY</strong>. This communication aims at '
                  'informing the user about new features or events related '
                  'to the Website, to received emails, to added friends, '
                  'to "likes", and so on…<strong>COGOFLY</strong> may '
                  'present new users of <strong>COGOFLY</strong> to the user. '
                  'It may also be the case that '
                  '<strong>COGOFLY</strong> presents the user as a '
                  'possible contact to other users of '
                  '<strong>COGOFLY</strong>. Finally, '
                  '<strong>COGOFLY</strong> may inform the user about other '
                  'users of <strong>COGOFLY</strong> who have visited the user'
                  '\'s profile or vice versa, i.e., the user may be one of '
                  'those users with regard to another user of '
                  '<strong>COGOFLY</strong> whose profile the user has '
                  'visited. Generally, the user may opt out of such '
                  'notifications through his/her individual personal '
                  'settings, though <strong>COGOFLY</strong> reserves the '
                  'right to send the user notices about his/her account.'),
            'privacy_policy_9_forwarding_information':
                _('9. Forwarding information to third parties:'),
            'privacy_policy_9_forwarding_information_details_1':
                _('<strong>COGOFLY</strong> does not forward the user\'s '
                  'personal data, his/her contents, or other information to '
                  'third parties without the user\'s consent, except where <'
                  'strong>COGOFLY</strong> believes such sharing is either 1) '
                  'necessary to use the Website or, 2) legally required or, 3'
                  ') permitted by the user. For example, <strong>COGOFLY</'
                  'strong> may forward personal data to service providers, to '
                  'its partners or sponsors, to help <strong>COGOFLY</strong> '
                  'offer a better service, a better access to and a better '
                  'use of the Website as a whole.'),
            'privacy_policy_9_forwarding_information_details_2':
                _('<strong>COGOFLY</strong> may be required to disclose '
                  'personal data by legal requests, such as court orders, in '
                  'compliance with applicable laws and regulations. '
                  'Additionally, <strong>COGOFLY</strong> may share '
                  'information when <strong>COGOFLY</strong> believes it is '
                  'necessary to comply with the law, to protect the interests '
                  'or property of <strong>COGOFLY</strong>, to prevent fraud '
                  'or other illegal activity perpetrated through the Website '
                  'or using the <strong>COGOFLY</strong> name, or to prevent '
                  'imminent damage. This may include sharing information with '
                  'other companies, lawyers, government agencies. By using '
                  'the Website or registering in the Website, the user allows '
                  '<strong>COGOFLY</strong> to process and use his/her '
                  'personal data for advertising or marketing purposes of '
                  'partners of <strong>COGOFLY</strong> via the Website. '
                  'Particularly, Personal Data may be used in order to tailor '
                  'the advertisement presented to the user to his/her '
                  'specific interests.'),
            'privacy_policy_10_miscellaneous':
                _('10. Miscellaneous:'),
            'privacy_policy_10_miscellaneous_1':
                _('10.1. Under Age:'),
            'privacy_policy_10_miscellaneous_1_details':
                _('Minors are not eligible to use the Website and are '
                  'therefore not allowed to register and submit any personal '
                  'information to <strong>COGOFLY</strong>. Parents and legal '
                  'guardians are responsible for the protection of their '
                  'children\'s privacy.'),
            'privacy_policy_10_miscellaneous_2':
                _('10.2. Links:'),
            'privacy_policy_10_miscellaneous_2_details':
                _('The Website may contain links to other websites. <strong>'
                  'COGOFLY</strong> is not responsible for the privacy '
                  'practices of other websites. <strong>COGOFLY</strong> '
                  'encourages the User to be aware when he/she leaves the '
                  'Website to read the privacy statements of each and every '
                  'website that collects personally identifiable information. '
                  'This Privacy Policy applies solely to information '
                  'collected by <strong>COGOFLY</strong>.'),
            'privacy_policy_11_changing_information':
                _('11. Changing or removing information:'),
            'privacy_policy_11_changing_information_details':
                _("The user may control most personal information via the "
                  "profile editing tools of his/her profile on the Website. "
                  "The user may modify or delete any of his/her profile "
                  "information except the mandatory information required "
                  "during the registration process at any time by logging "
                  "into his/her account. Information will be updated "
                  "immediately, subject to have saved it. Users who wish to "
                  "deactivate their account with <strong>COGOFLY</strong> "
                  "should act as mentioned in article Deactivation or "
                  "deletion of an account of the Terms and Conditions. In "
                  "this case, <strong>COGOFLY</strong> will remove the "
                  "user's "
                  "name and other personally identifiable information from "
                  "publicly viewable data. However, <strong>COGOFLY</strong> "
                  "may retain certain data contributed by the user if it may "
                  "be necessary to prevent fraud or future abuse, or for "
                  "legitimate business purposes, such as statistical analysis "
                  "of non-personally-identifiable data, or if required by law"
                  ". All retained data will continue to be subject to the "
                  "terms of the Privacy Policy that the user has previously "
                  "agreed to. Where the user makes use of the communication "
                  "features of the service to share information with other "
                  "users of <strong>COGOFLY</strong>, however, (e.g., sending "
                  "a personal message to another user of "
                  "<strong>COGOFLY</strong>) the user generally cannot remove "
                  "such communications."),
            'privacy_policy_12_litigation':
                _('12. Litigation:'),
            'privacy_policy_12_litigation_details':
                _('Any dispute arising from the use of the Website is subject '
                  'to this Privacy Policy and to the Terms and Conditions, '
                  'including limitation of liability.'),
            'privacy_policy_13_modification':
                _('13. Modification of Privacy Policy:'),
            'privacy_policy_13_modification_details':
                _('<strong>COGOFLY</strong> reserves the right to amend this '
                  'Privacy Policy at any time. <strong>COGOFLY</strong> shall '
                  'give due notice of any amendments of this Privacy Policy '
                  'to the user via the user\'s email address or by placing a '
                  'notice in the user\'s personal inbox on the Website.'),
        })
