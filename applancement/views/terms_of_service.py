# coding=UTF-8
# Conditions d'utilisation pour cogofly


from django.shortcuts import render
from django.views.generic import View
from django.utils.translation import ugettext as _


class TermsOfServiceView(View):
    template_name = 'static/terms_of_service.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'tos_title': _('Cogofly - Terms of service'),
            'tos_contact_us': _(
                'If you require any more information or have any questions '
                'about our Terms of Service, please feel free to contact '
                'us by email by clicking '
                '<a href="mailto:cogofly@gmail.com" target="_blank">'
                'here '
                '</a>'),
            'tos_introduction': _('Introduction'),
            'tos_introduction_1': _(
                'These terms and conditions govern your use of this website;'
                'by using this website, you accept these terms and conditions '
                'in full and without reservation. If you disagree with these '
                'terms and conditions or any part of these terms and '
                'conditions, you must not use this website.'),
            'tos_introduction_2': _(
                'You must be at least 18 [eighteen] years of age to use this '
                'website. By using this website and by agreeing to these '
                'terms and conditions, you warrant and represent that you are '
                'at least 18 years of age.'),
            'tos_licence': _('License to use website'),
            'tos_licence_1': _(
                'Unless otherwise stated,'
                '<a href="/" target="_blank">www.cogofly.com</a>'
                'and/or its licensors own the intellectual property rights '
                'published on this website and materials used on '
                '<a href="/" target="_blank">www.cogofly.com</a>.'
                'Subject to the license below, all these intellectual '
                'property rights are reserved.'),
            'tos_licence_2': _(
                'You may view, download for caching purposes only,'
                'and print pages, files or other content from the website '
                'for your own personal use, subject to the restrictions set '
                'out below and elsewhere in these terms and conditions.'
            ),
            'tos_licence_you_must_not': {
                'title': _(
                    'You must not:'
                ),
                'tab': [
                    _('republish material from this website in neither '
                      'print nor digital media or documents (including '
                      'republication on another website);'),
                    _('sell, rent or sub-license material from the website;'),
                    _('show any material from the website in public;'),
                    _('reproduce, duplicate, copy or otherwise exploit '
                      'material on this website for a commercial purpose;'),
                    _('edit or otherwise modify any material on the website;'),
                    _('redistribute material from this website - except '
                      'for content specifically and expressly made available '
                      'for redistribution; or'),
                    _('republish or reproduce any part of this website '
                      'through the use of iframes or screenscrapers.'),
                ],
            },
            'tos_content_redistribution': _(
                'Where content is specifically made available for '
                'redistribution, it may only be redistributed within your '
                'organisation.'),
            'tos_acceptable_use': {
                'title': _('Acceptable use'),
                'tab': [
                    _('You must not use this website in any way that causes, '
                      'or may cause, damage to the website or impairment of '
                      'the availability or accessibility of '
                      '<a href="/" target="_blank">www.cogofly.com</a> '
                      'or in any way which is unlawful, illegal, fraudulent '
                      'or harmful, or in connection with any unlawful, '
                      'illegal, fraudulent or harmful purpose or activity.'),
                    _('You must not use this website to copy, store, host, '
                      'transmit, send, use, publish or distribute any '
                      'material which consists of (or is linked to) any '
                      'spyware, computer virus, Trojan horse, worm, keystroke '
                      'logger, rootkit or other malicious computer software.'),
                    _('You must not conduct any systematic or automated '
                      'data collection activities on or in relation to this '
                      'website without <a href="/" target="_blank">'
                      'www.cogofly.com\'s'
                      '</a> express written consent. This includes:')
                ]
            },
            'tos_acceptable_this_includes_tab': [
                _('scraping'),
                _('data mining'),
                _('data extraction'),
                _('data harvesting'),
                _('"framing" (iframes)'),
                _('Article "Spinning"'),
            ],
            'tos_you_must_not_use_1':
                _('You must not use this website or any part of it to '
                  'transmit or send unsolicited commercial communications.'),
            'tos_you_must_not_use_2':
                _('You must not use this website for any purposes related to '
                  'marketing without the express written consent of '
                  '<a href="/" target="_blank">www.cogofly.com</a>.'),
            'tos_restricted_access_title': _('Restricted access'),
            'tos_restricted_access_1':
                _('Access to certain areas of this '
                  'website is restricted.'
                  '<a href="/" target="_blank">www.cogofly.com</a> reserves '
                  'the right to restrict access to certain areas of this '
                  'website, or at our discretion, this entire website.'
                  '<a href="/" target="_blank">www.cogofly.com</a> may change '
                  'or modify this policy without notice.'),
            'tos_restricted_access_2':
                _('If <a href="/" target="_blank">www.cogofly.com</a>'
                  'provides you with a user ID and password to enable you to '
                  'access restricted areas of this website or other content '
                  'or services, you must ensure that the user ID and password '
                  'are kept confidential. You alone are responsible for your '
                  'password and user ID security.'),
            'tos_restricted_access_3':
                _('<a href="/" target="_blank">www.cogofly.com</a> may '
                  'disable your user ID and password at '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> sole '
                  'discretion without notice or explanation.'),
            'tos_user_content': _('User content'),
            'tos_user_content_1':
                _('In these terms and conditions, "your user content"'
                  'means material (including without limitation text, images,'
                  'audio material, video material and audio-visual material) '
                  'that you submit to this website, for whatever purpose.'),
            'tos_user_content_2':
                _('You grant to '
                  '<a href="/" target="_blank">www.cogofly.com</a> a '
                  'worldwide, irrevocable, non-exclusive, royalty-free '
                  'license to use, reproduce, adapt, publish, translate and '
                  'distribute your user content in any existing or future '
                  'media.  You also grant to '
                  '<a href="/" target="_blank">www.cogofly.com</a> the right '
                  'to sub-license these rights, and the right to bring an '
                  'action for infringement of these rights.'),
            'tos_user_content_3':
                _('Your user content must not be illegal or unlawful, must '
                  'not infringe any third party\'s legal rights, and must not '
                  'be capable of giving rise to legal action whether against '
                  'you or '
                  '<a href="/" target="_blank">www.cogofly.com</a> or a third '
                  'party (in each case under any applicable law).'),
            'tos_user_content_4':
                _('You must not submit any user content to the website that '
                  'is or has ever been the subject of any threatened or '
                  'actual legal proceedings or other similar complaint.'),
            'tos_user_content_5':
                _('<a href="/" target="_blank">www.cogofly.com</a> reserves '
                  'the right to edit or remove any material submitted to this '
                  'website, or stored on the servers of '
                  '<a href="/" target="_blank">www.cogofly.com</a>, or hosted '
                  'or published upon this website.'),
            'tos_user_content_6':
                _('<a href="/" target="_blank">www.cogofly.com\'s</a> rights '
                  'under these terms and conditions in relation to user '
                  'content,'
                  '<a href="/" target="_blank">www.cogofly.com</a> does not '
                  'undertake to monitor the submission of such content to, or '
                  'the publication of such content on, this website.'),
            'tos_no_warranties_title': _('No warranties'),
            'tos_no_warranties_1':
                _('This website is provided "as is" without any '
                  'representations or warranties, express or implied.'
                  '<a href="/" target="_blank">www.cogofly.com</a> makes no '
                  'representations or warranties in relation to this website '
                  'or the information and materials provided on this '
                  'website.'),
            'tos_no_warranties_2':
                _('Without prejudice to the generality of the foregoing '
                  'paragraph, <a href="/" target="_blank">www.cogofly.com</a>'
                  ' does not warrant that:'),
            'tos_no_warranties_2_1':
                _('this website will be constantly available, or available '
                  'at all; or'),
            'tos_no_warranties_2_2':
                _('the information on this website is complete, true, '
                  'accurate or non-misleading.'),
            'tos_no_warranties_3':
                _('Nothing on this website constitutes, or is meant to '
                  'constitute, advice of any kind. If you require advice in '
                  'relation to any legal, financial or medical matter you '
                  'should consult an appropriate professional.'),
            'tos_liability_title': _('Limitations of liability'),
            'tos_liability_1':
                _('<a href="/" target="_blank">www.cogofly.com</a> will not '
                  'be liable to you (whether under the law of contact, the '
                  'law of torts or otherwise) in relation to the contents of, '
                  'or use of, or otherwise in connection with, this website:'),
            'tos_liability_1_1':
                _('to the extent that the website is provided free-of-charge,'
                  'for any direct loss;'),
            'tos_liability_1_2':
                _('for any indirect, special or consequential loss; or'),
            'tos_liability_1_3':
                _('for any business losses, loss of revenue, income, profits '
                  'or anticipated savings, loss of contracts or business '
                  'relationships, loss of reputation or goodwill, or loss or '
                  'corruption of information or data.'),
            'tos_liability_2':
                _('These limitations of liability apply even if '
                  '<a href="/" target="_blank">www.cogofly.com</a> has been '
                  'expressly advised of the potential loss.'),
            'tos_exceptions_title': _('Exceptions'),
            'tos_exceptions_1':
                _('Nothing in this website disclaimer will exclude or limit '
                  'any warranty implied by law that it would be unlawful to '
                  'exclude or limit; and nothing in this website disclaimer '
                  'will exclude or limit the liability of Cogofly in respect '
                  'of any:'),
            'tos_exceptions_1_1':
                _('death or personal injury caused by the negligence of '
                  '<a href="/" target="_blank">www.cogofly.com</a> or its '
                  'agents, employees or shareholders/owners;'),
            'tos_exceptions_1_2':
                _('fraud or fraudulent misrepresentation on the part of '
                  '<a href="/" target="_blank">www.cogofly.com</a>; or'),
            'tos_exceptions_1_3':
                _('matter which it would be illegal or unlawful for '
                  '<a href="/" target="_blank">www.cogofly.com</a> to exclude '
                  'or limit, or to attempt or purport to exclude or limit, '
                  'its liability.'),
            'tos_reasonableness_title': _('Reasonableness'),
            'tos_reasonableness_1':
                _('By using this website, you agree that the exclusions and '
                  'limitations of liability set out in this website '
                  'disclaimer are reasonable.'),
            'tos_reasonableness_2':
                _('If you do not think they are reasonable, you must not use '
                  'this website.'),
            'tos_other_parties_title': _('Other parties'),
            'tos_other_parties_1':
                _('You accept that, as a limited liability entity,'
                  '<a href="/" target="_blank">www.cogofly.com</a> has an '
                  'interest in limiting the personal liability of its '
                  'officers and employees. You agree that you will not bring '
                  'any claim personally against '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> '
                  'officers or employees in respect of any losses you suffer '
                  'in connection with the website.'),
            'tos_other_parties_2':
                _('Without prejudice to the foregoing paragraph, you agree '
                  'that the limitations of warranties and liability set out '
                  'in this website disclaimer will protect '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> '
                  'officers, employees, agents, subsidiaries, successors, '
                  'assigns and sub-contractors as well as '
                  '<a href="/" target="_blank">www.cogofly.com</a>.'),
            'tos_unenforceable_provisions_title':
                _('Unenforceable provisions'),
            'tos_unenforceable_provisions_1':
                _('If any provision of this website disclaimer is, or is '
                  'found to be, unenforceable under applicable law, that will '
                  'not affect the enforceability of the other provisions of '
                  'this website disclaimer.'),
            'tos_indemnity_title': _('Indemnity'),
            'tos_indemnity_1':
                _('You hereby indemnify '
                  '<a href="/" target="_blank">www.cogofly.com</a> and '
                  'undertake to keep '
                  '<a href="/" target="_blank">www.cogofly.com</a>'
                  'indemnified against any losses, damages, costs, '
                  'liabilities and expenses (including without limitation '
                  'legal expenses and any amounts paid by '
                  '<a href="/" target="_blank">www.cogofly.com</a> to a third '
                  'party in settlement of a claim or dispute on the advice of '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a>'
                  'legal advisers) incurred or suffered by '
                  '<a href="/" target="_blank">www.cogofly.com</a> arising '
                  'out of any breach by you of any provision of these terms '
                  'and conditions, or arising out of any claim that you have '
                  'breached any provision of these terms and conditions.'),
            'tos_breaches_title': _('Breaches of these terms and conditions'),
            'tos_breaches_1':
                _('Without prejudice to '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> other '
                  'rights under these terms and conditions, if you breach '
                  'these terms and conditions in any way, '
                  '<a href="/" target="_blank">www.cogofly.com</a> may take '
                  'such action as '
                  '<a href="/" target="_blank">www.cogofly.com</a> deems '
                  'appropriate to deal with the breach, including suspending '
                  'your access to the website, prohibiting you from accessing '
                  'the website, blocking computers using your IP address from '
                  'accessing the website, contacting your internet service '
                  'provider to request that they block your access to the '
                  'website and/or bringing court proceedings against you.'),
            'tos_variation_title': _('Variation'),
            'tos_variation_1':
                _('<a href="/" target="_blank">www.cogofly.com</a> may revise '
                  'these terms and conditions from time-to-time. Revised '
                  'terms and conditions will apply to the use of this website '
                  'from the date of the publication of the revised terms and '
                  'conditions on this website. Please check this page '
                  'regularly to ensure you are familiar with the current '
                  'version.'),
            'tos_assignment_title': _('Assignment'),
            'tos_assignment_1':
                _('<a href="/" target="_blank">www.cogofly.com</a> may '
                  'transfer, sub-contract or otherwise deal with '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> rights '
                  'and/or obligations under these terms and conditions '
                  'without notifying you or obtaining your consent.'),
            'tos_assignment_2':
                _('You may not transfer, sub-contract or otherwise deal with '
                  'your rights and/or obligations under these terms and '
                  'conditions.'),
            'tos_severability_title': _('Severability'),
            'tos_severability_1':
                _('If a provision of these terms and conditions is determined '
                  'by any court or other competent authority to be unlawful '
                  'and/or unenforceable, the other provisions will continue '
                  'in effect. If any unlawful and/or unenforceable provision '
                  'would be lawful or enforceable if part of it were deleted, '
                  'that part will be deemed to be deleted, and the rest of '
                  'the provision will continue in effect.'),
            'tos_entire_agreement_title': _('Entire agreement'),
            'tos_entire_agreement_1':
                _('These terms and conditions, together with '
                  '<a href="/" target="_blank">www.cogofly.com\'s</a> Privacy '
                  'Policy constitute the entire agreement between you and '
                  '<a href="/" target="_blank">www.cogofly.com</a> in '
                  'relation to your use of this website, and supersede all '
                  'previous agreements in respect of your use of this '
                  'website.'),
            'tos_law_and_juridiction_title': _('Law and jurisdiction'),
            'tos_law_and_juridiction_1':
                _('These terms and conditions will be governed by and '
                  'construed in accordance with the laws of Marseille '
                  '(France), and any disputes relating to these terms and '
                  'conditions will be subject to the exclusive jurisdiction '
                  'of the courts of '
                  'Marseille (France).'),
            'tos_about_title': _('About these website Terms of Service'),
            'tos_about_1':
                _('We created these website terms and conditions using '
                  'the TOS/T&amp;C generator available from '
                  '<a href="http://www.privacypolicyonline.com/" '
                  'target="_blank">'
                  'Privacy Policy Online '
                  '</a>.'),
            'tos_about_2':
                _('<a href="//" target="_blank">'
                  'www.cogofly.com\'s'
                  '</a>'
                  'registration number is SIREN '
                  'n°&nbsp;441&nbsp;715&nbsp;612&nbsp;/'
                  'SIRET n°441&nbsp;715&nbsp;612&nbsp;00020.'),
            'tos_about_3':
                _('<a href="//" target="_blank">'
                  'www.cogofly.com</a>'
                  'subscribes to the following code(s) of conduct:<br />'
                  '<strong>'
                  'We are registered at the CNIL under file no. 1822236'
                  '</strong>'),
            'tos_details_title':
                _('<a href="//" target="_blank">'
                'www.cogofly.com\'s</a> details'),
            'tos_details_1':
                _('The full name of '
                  '<a href="//" target="_blank">'
                  'www.cogofly.com'
                  '</a> is Cogofly.'),
            'tos_details_2':
                _('<a href="//" target="_blank">'
                  'www.cogofly.com</a> is registered in Marseille (France) '
                  'under registration number SIREN n° 441&nbsp;715&nbsp;612 /'
                  'SIRET n°&nbsp;441&nbsp;715&nbsp;612&nbsp;00020.'),
            'tos_other_title': _('OTHER TITLE'),
            'tos_other_1':
                _('<a href="http://www.privacypolicyonline.com/"'
                  'title="PrivacyPolicyOnline.com Approved Site"'
                  'alt="Privacy Policy Online Approved Site">'
                  '<strong>URSSAF PACA n° U13072489971</strong></a>'),
            'tos_other_2':
                _('You can contact '
                  '<a href="//" target="_blank">'
                  'www.cogofly.com</a> by email at our email address link at '
                  'the top of this Terms of Service document.'),
        })


