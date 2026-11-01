import json
import re
import unittest
from email.utils import parsedate_to_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class NovemberIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = json.loads((ROOT / 'data/november-sources.json').read_text())
        cls.base = json.loads((ROOT / 'data/sources.json').read_text())
        cls.by_id = {r['id']: r for r in cls.sources}

    def test_existing_critical_thinking_paper_is_updated_not_duplicated(self):
        updates = json.loads((ROOT / 'november/source-updates.json').read_text())
        self.assertEqual(updates['target_release'], '2026-11')
        self.assertEqual(updates['status'], 'pending-editorial-promotion')
        existing = {r['id'] for r in self.base}
        ids = [r['id'] for r in updates['records']]
        self.assertEqual(len(ids), len(set(ids)))
        taxonomy = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())
        for update in updates['records']:
            self.assertIn(update['id'], existing)
            self.assertNotIn(update['id'], self.by_id)
            fields = update['fields']
            self.assertEqual(fields['verification']['checked_on'], update['checked_on'])
            self.assertLessEqual(fields['date'], update['checked_on'])
            self.assertFalse(set(fields['topics']) - set(taxonomy['topics']))
        paper = next(r['fields'] for r in updates['records'] if r['id'] == 'ref-712e3405f2')
        self.assertEqual(paper['doi'], '10.1145/3706598.3713778')
        self.assertEqual(len(paper['authors']), 7)
        self.assertEqual(paper['date'], '2025-04')
        self.assertIn('not an objective skill test', paper['limitations'])
        self.assertEqual(paper['document_snapshot']['version'], 'author-version')
        self.assertFalse(paper['document_snapshot']['redistributed'])
        self.assertIn('403', paper['verification']['basis'])

    def test_postgres_release_notices_do_not_establish_ai_causality(self):
        account = self.by_id['haaspostgres2026']
        beta = self.by_id['pg19beta42026']
        rc = self.by_id['pg19rc12026']
        self.assertEqual(account['authors'], ['Haas, Robert'])
        self.assertEqual(account['date'], '2026-10-21')
        self.assertEqual(beta['date'], '2026-09-24')
        self.assertEqual(rc['date'], '2026-10-15')
        self.assertEqual(len({r['study_family'] for r in [account, beta, rc]}), 1)
        self.assertIn('neither unique defect counts', account['limitations'])
        self.assertIn('not independently rerun', account['limitations'])
        self.assertIn('Does not attribute', beta['limitations'])
        self.assertIn('not evidence', rc['limitations'])
        self.assertIn('19 November', rc['summary'])
        for source in [beta, rc]:
            self.assertEqual(source['publication_status'], 'project-release-notice')

    def test_cisco_proposal_is_not_a_completed_productivity_result(self):
        source = self.by_id['roylecisco2026']
        self.assertEqual(source['authors'], ['Royle, Orianna Rosa'])
        self.assertEqual(source['date'], '2026-10-30')
        self.assertEqual(source['publication_status'], 'journalism')
        self.assertEqual(source['method'], 'executive-interview-reporting')
        self.assertIn('not demonstrated delivery', source['summary'])
        self.assertIn('not a representative sample', source['limitations'])
        self.assertIn('not independent confirmation', source['verification']['basis'])
        self.assertIn('terkowitzrole2026', source['related_to'])
        self.assertTrue({'engineering', 'work', 'cost', 'quality'}.issubset(source['topics']))

    def test_amazon_guidance_is_policy_not_a_productivity_estimate(self):
        source = self.by_id['terkowitzrole2026']
        self.assertEqual(source['authors'], ['Terkowitz, Terk'])
        self.assertEqual(source['date'], '2026-10-27')
        self.assertEqual(source['publication_status'], 'company-policy-commentary')
        self.assertEqual(source['method'], 'corporate-engineering-leadership-memo')
        self.assertIn('does not help', source['summary'])
        self.assertIn('do not establish causality', source['limitations'])
        self.assertIn('complete guideline', source['limitations'])
        self.assertTrue({'engineering', 'governance', 'learning', 'methods'}.issubset(source['topics']))
        self.assertEqual(source['verification']['checked_on'], '2026-11-01')

    def test_cross_topic_search_has_resolvable_selections_and_reading_scopes(self):
        log = json.loads((ROOT / 'november/search-2026-10-28.json').read_text())
        self.assertEqual(log['searched_on'], '2026-10-28')
        selected = log['selected_ids']
        self.assertEqual(log['selected_count'], len(selected))
        self.assertEqual(len(selected), len(set(selected)))
        self.assertTrue(set(log['full_text_follow_up_ids']).issubset(selected))
        available = {r['id'] for r in self.base}
        self.assertTrue({r['id'] for r in log['known_not_duplicated']}.issubset(available))
        for key in selected:
            source = self.by_id[key]
            self.assertEqual(source['verification']['checked_on'], log['searched_on'])
            self.assertTrue(source['reading_scope'])
            self.assertTrue(source['limitations'])
            self.assertTrue(source.get('doi') or source.get('arxiv_id') or source['date_basis'])
        topics = {topic for key in selected for topic in self.by_id[key]['topics']}
        self.assertTrue({'learning', 'science', 'work', 'business', 'engineering',
                         'diversity', 'sustainability'}.issubset(topics))

    def test_cross_topic_revision_and_method_boundaries(self):
        firm = self.by_id['yotzovfirm2026']
        self.assertEqual(firm['date'], '2026-02')
        self.assertEqual(firm['revision_date'], '2026-10')
        self.assertEqual(len(firm['authors']), 17)
        self.assertIn('9,000', firm['summary'])
        self.assertIn('forecasts', firm['limitations'])
        self.assertIn('not actual rerunning', self.by_id['coakleyrepro2026']['limitations'])
        self.assertIn('Not a test of transfer without AI',
                      self.by_id['kewenigscaffolds2026']['limitations'])
        self.assertIn('preprint', self.by_id['ferinodelegation2026']['publication_status'])
        self.assertEqual(self.by_id['mockuscontext2026']['publication_status'], 'conference-paper')
        self.assertEqual(self.by_id['oviedoenergy2026']['study_family'],
                         self.by_id['myttonenergy2026']['study_family'])

    def test_calegari_guest_authorship_is_not_the_platform_host(self):
        source = self.by_id['calegarichanged2026']
        self.assertEqual(source['authors'], ['Calegari, Frank'])
        self.assertEqual(source['date'], '2026-11-01')
        self.assertEqual(source['verification']['checked_on'], '2026-11-01')
        self.assertEqual(source['method'], 'expert-normative-commentary')
        self.assertEqual(source['publication_status'], 'guest-blog-post')
        self.assertTrue({'mathematics', 'science', 'learning', 'governance'}.issubset(source['topics']))
        self.assertIn('not a causal study', source['limitations'])

    def test_november_four_article_intake_preserves_roles_and_primary_families(self):
        explainer = self.by_id['millscreativity2026']
        paper = self.by_id['zoranbecoming2026']
        self.assertEqual(explainer['authors'], ['Mills, Yarden'])
        self.assertEqual(explainer['editors'], ['Cohen, Shy'])
        self.assertEqual(paper['doi'], '10.1007/s00146-026-03379-x')
        self.assertEqual(explainer['study_family'], paper['study_family'])
        report = self.by_id['vanoosteromcuts2026']
        policy = self.by_id['dutchrestructuring2026']
        self.assertEqual(report['study_family'], policy['study_family'])
        self.assertNotIn('?', report['url'])
        self.assertIn('FTE', policy['summary'])
        self.assertIn('2027', policy['summary'])
        self.assertEqual(report['reading_scope'], 'publisher-metadata-and-public-opening-only')
        self.assertEqual(self.by_id['mckinseyroi2026']['date'], '2026-08-25')
        self.assertIn('not equivalent to project failure',
                      self.by_id['mckinseyroi2026']['limitations'])
        self.assertIn('not independently read', self.by_id['coffeefailure2026']['limitations'])

    def test_quantum_reporting_does_not_validate_a_millennium_solution(self):
        report = self.by_id['howlettquantum2026']
        self.assertEqual(report['authors'], ['Howlett, Joseph'])
        self.assertEqual(report['publication_status'], 'journalism')
        self.assertIn('narrower', report['summary'])
        self.assertIn('not proof verification', report['limitations'])
        self.assertIn('openaiunderstanding2026', report['related_to'])
        self.assertIn('quantum-math-problem', report['url'])
        self.assertNotEqual(report['title'], report['alternate_title'])

    def test_wikimedia_filing_identity_and_procedural_status(self):
        brief = self.by_id['wmfbrief2026']
        statement = self.by_id['wmfknowledge2026']
        report = self.by_id['feinerwikimedia2026']
        self.assertEqual(brief['date'], '2026-10-29')
        self.assertEqual(statement['date'], '2026-10-30')
        self.assertEqual(brief['court_identifiers']['proposed_brief'], '2361-1')
        self.assertEqual(brief['publication_status'], 'court-filing-not-a-ruling')
        self.assertEqual(len({r['study_family'] for r in [brief, statement, report]}), 1)
        self.assertIn('Footnote 24', brief['summary'])
        self.assertIn('not a court decision', statement['limitations'])
        self.assertEqual(report['authors'], ['Feiner, Lauren'])

    def test_eth_news_is_not_proof_validation_and_access_is_scoped(self):
        report = self.by_id['howartheth2026']
        self.assertEqual(report['authors'], ['Howarth, Tom'])
        self.assertEqual(report['date'], '2026-10-28')
        self.assertEqual(report['doi'], '10.1126/science.z3zo39t')
        self.assertEqual(report['publication_status'], 'journalism')
        self.assertIn('not a peer-reviewed proof', report['limitations'])
        observations = {r['id']: r for r in json.loads(
            (ROOT / 'november/browser-observations.json').read_text())['observations']}
        for key in ['howartheth2026', 'feinerwikimedia2026']:
            self.assertFalse(observations[key]['full_text_read'])
            self.assertEqual(observations[key]['inspection_date'], '2026-11-01')

    def test_memory_allocation_argument_is_not_an_efficiency_benchmark(self):
        report = self.by_id['bonifieldram2026']
        supplier = self.by_id['skhynixsupply2026']
        self.assertEqual(report['authors'], ['Bonifield, Stevie'])
        self.assertEqual(report['date'], '2026-10-30')
        self.assertEqual(supplier['date'], '2026-10-28')
        self.assertIn('not a comparative cloud/local benchmark', report['limitations'])
        self.assertIn('Company capacity is not global output', supplier['limitations'])
        self.assertIn('not watched', report['limitations'])
        self.assertEqual(report['publication_status'], 'journalism')
        self.assertEqual(supplier['publication_status'], 'company-earnings-release')

    def test_altman_math_remarks_share_interview_family_not_independent_validation(self):
        source = self.by_id['hartaltmanmath2026']
        self.assertEqual(source['authors'], ['Hart, Robert'])
        self.assertEqual(source['date'], '2026-10-30')
        self.assertEqual(source['publication_status'], 'journalism')
        self.assertEqual(source['study_family'], self.by_id['bonifieldram2026']['study_family'])
        self.assertIn('not proof validation', source['limitations'])
        self.assertIn('Original interview not watched', source['limitations'])
        self.assertIn('hartaltmanmath2026', self.by_id['bonifieldram2026']['related_to'])

    def test_recruiting_claims_keep_primary_date_and_historical_method(self):
        report = self.by_id['clarkrecruiting2026']
        transcript = self.by_id['accenturetalent2026']
        critique = self.by_id['dragemackereth2022']
        self.assertEqual(report['authors'], ['Clark, Lindsay'])
        self.assertEqual(transcript['date'], '2026-10-14')
        self.assertEqual(transcript['year'], 2026)
        self.assertEqual(report['study_family'], transcript['study_family'])
        self.assertIn('28%', transcript['summary'])
        self.assertIn('30%', transcript['summary'])
        self.assertIn('not an independent test of durable skill', transcript['limitations'])
        self.assertEqual(critique['doi'], '10.1007/s13347-022-00543-1')
        self.assertEqual(critique['date'], '2022-10-10')
        self.assertEqual(critique['method'], 'critical-theoretical-analysis-of-recruitment-marketing')
        self.assertIn('not a randomized hiring-outcome study', critique['limitations'])

    def test_ambition_gap_is_commissioned_synthesis_not_a_payoff_guarantee(self):
        report = self.by_id['vanarkambition2026']
        news = self.by_id['robinsonambition2026']
        self.assertEqual(report['authors'], ['van Ark, Bart', 'Karountzos, Vassilis'])
        self.assertEqual(report['date'], '2026-10-29')
        self.assertEqual(news['date'], '2026-10-30')
        self.assertEqual(news['authors'], ['Robinson, Dan'])
        self.assertEqual(report['study_family'], news['study_family'])
        self.assertEqual(report['method'], 'narrative-evidence-synthesis-and-expert-interviews')
        self.assertIn('not a new causal trial', report['limitations'])
        self.assertIn('do not establish inevitable payoff', report['limitations'])
        self.assertIn('Bytes', report['container_title'])
        snapshot = report['document_snapshot']
        self.assertEqual(snapshot['pages'], 44)
        self.assertEqual(snapshot['bytes'], 4275794)
        self.assertRegex(snapshot['sha256'], r'^[a-f0-9]{64}$')
        self.assertFalse(snapshot['redistributed'])

    def test_cross_topic_new_dois_do_not_duplicate_existing_studies(self):
        log = json.loads((ROOT / 'november/search-2026-10-28.json').read_text())
        selected = set(log['selected_ids'])
        normalize = lambda value: value.lower().removeprefix('https://doi.org/').strip()
        prior = {normalize(r['doi']) for r in self.base + self.sources
                 if r.get('doi') and r['id'] not in selected}
        new = [normalize(self.by_id[key]['doi']) for key in selected
               if self.by_id[key].get('doi')]
        self.assertEqual(len(new), len(set(new)))
        self.assertFalse(set(new) & prior)

    def test_unique_staged_identities_and_scope(self):
        self.assertEqual(len(self.sources), len(self.by_id))
        self.assertEqual(len(self.sources), len({r['url'] for r in self.sources}))
        self.assertFalse(set(self.by_id) & {r['id'] for r in self.base})
        taxonomy = json.loads((ROOT / 'data/topic-taxonomy.json').read_text())
        for source in self.sources:
            self.assertEqual(source['target_release'], '2026-11')
            self.assertEqual(source['staging_status'], 'appraised-not-yet-published')
            self.assertEqual(source['verification']['level'], 'content-checked')
            self.assertTrue(source['verification']['basis'])
            self.assertLessEqual(source['date'], source['verification']['checked_on'])
            self.assertFalse(set(source['topics']) - set(taxonomy['topics']))

    def test_draft_citations_resolve_without_expanding_october(self):
        draft = '\n'.join(path.read_text() for path in (ROOT / 'manuscript').glob('november-*.md'))
        ids = {item.strip().lstrip('@') for group in re.findall(r'\[@([^\]]+)\]', draft)
               for item in group.split(';')}
        available = set(self.by_id) | {r['id'] for r in self.base}
        self.assertFalse(ids - available)
        self.assertIn('torvaldstools2026', ids)
        self.assertIn('pincharttools2026', ids)
        self.assertIn('cooktools2026', ids)
        self.assertIn('luuambitious2026', ids)
        for source in self.sources:
            for related in source['related_to']:
                self.assertIn(related, available)

    def test_alternative_checks_are_not_november_receipts(self):
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        self.assertEqual(ledger['target_release'], '2026-11')
        self.assertFalse(ledger['release_receipts_complete'])
        self.assertIn(ledger['method'], ['local-chrome-native', 'local-chrome-mixed'])
        for observation in ledger['observations']:
            self.assertIn(observation['id'], self.by_id)
            self.assertEqual(observation['source_url'], self.by_id[observation['id']]['url'])
            self.assertTrue(observation['refresh_required'])

    def test_policies_are_rechecks_not_duplicate_sources(self):
        rechecks = json.loads((ROOT / 'data/november-source-rechecks.json').read_text())
        self.assertRegex(rechecks['upstream_revision'], r'^[a-f0-9]{40}$')
        existing = {r['id'] for r in self.base}
        for record in rechecks['records']:
            self.assertIn(record['id'], existing)
            self.assertNotIn(record['id'], self.by_id)
            self.assertIn(rechecks['upstream_revision'], record['inspected_url'])

    def test_essay_date_uses_publisher_metadata(self):
        source = self.by_id['luuambitious2026']
        observation = source['metadata_observation']
        self.assertEqual(observation['guid'], source['url'])
        self.assertEqual(parsedate_to_datetime(observation['pubDate']).date().isoformat(), source['date'])
        self.assertEqual(observation['feed_type'], 'rss')
        self.assertEqual(source['method'], 'expert-commentary')

    def test_restricted_reading_scopes_and_article_metadata(self):
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        observations = {r['id']: r for r in ledger['observations']}
        self.assertFalse(observations['strogatzfuture2026']['full_text_read'])
        self.assertTrue(observations['baimehomework2026']['full_text_read'])
        self.assertEqual(self.by_id['baimehomework2026']['authors'], ['Baime, Audrey'])
        self.assertEqual(self.by_id['baimehomework2026']['date'], '2026-10-23')
        for observation in ledger['observations']:
            self.assertLessEqual(ledger['created_on'], observation['inspection_date'])
            self.assertLessEqual(observation['inspection_date'], ledger['updated_on'])
            self.assertEqual(observation['inspection_date'],
                             self.by_id[observation['id']]['verification']['checked_on'])
        self.assertEqual(self.by_id['slokpayoff2026']['admission_decision'],
                         'include-as-critical-macro-context-not-causal-null')

    def test_price_snapshot_has_explicit_units_and_token_categories(self):
        snapshot = self.by_id['opus55pricing2026']['pricing_snapshot']
        self.assertEqual(snapshot['unit'], 'per-million-tokens')
        self.assertEqual(snapshot['currency'], 'USD')
        self.assertEqual({k: snapshot[k] for k in ['standard_input', 'standard_output', 'cache_read', 'cache_write']},
                         {'standard_input': 4, 'standard_output': 20, 'cache_read': 0.2, 'cache_write': 5})
        self.assertEqual(self.by_id['vercelindex2026']['method'], 'commercial-platform-telemetry')

    def test_full_text_document_check_preserves_browser_history(self):
        ledger = json.loads((ROOT / 'november/document-observations.json').read_text())
        self.assertEqual(ledger['target_release'], '2026-11')
        self.assertFalse(ledger['release_receipts_complete'])
        observation = next(r for r in ledger['observations'] if r['id'] == 'strogatzfuture2026')
        source = self.by_id[observation['id']]
        document = source['document_verification']
        self.assertTrue(observation['full_text_read'])
        self.assertEqual(observation['source_url'], source['url'])
        self.assertEqual(observation['inspection_date'], document['checked_on'])
        self.assertEqual(observation['inspection_date'], source['verification']['checked_on'])
        self.assertLessEqual(ledger['created_on'], observation['inspection_date'])
        self.assertRegex(document['sha256'], r'^[a-f0-9]{64}$')
        for key in ['filename', 'sha256', 'pages', 'redistributed']:
            self.assertEqual(observation[key], document[key])
        self.assertEqual(document['pages'], 10)
        self.assertFalse(document['redistributed'])
        self.assertTrue(document['scope'])
        self.assertTrue(observation['refresh_required'])
        self.assertEqual(source['authors'], ['Strogatz, Steven'])
        self.assertEqual(source['method'], 'expert-perspective')
        self.assertEqual(source['admission_decision'],
                         'include-full-text-expert-perspective-not-proof-validation')

    def test_syndicated_reuters_is_one_identified_report(self):
        report = self.by_id['reutersitcontracts2026']
        self.assertEqual(report['publisher'], 'Reuters')
        self.assertTrue(report['original_url'].startswith('https://www.reuters.com/'))
        self.assertTrue(report['url'].startswith('https://www.thestar.com.my/'))
        self.assertEqual(report['date'], '2026-08-21')
        self.assertEqual(sum(r.get('study_family') == report['study_family'] for r in self.sources), 1)

    def test_latest_intake_differentiates_methods_and_stable_identity(self):
        self.assertEqual(self.by_id['vandenbergagents2026']['authors'], ['van den Berg, Jan'])
        self.assertEqual(self.by_id['voytkoquality2026']['authors'], ['Voytko, Jake'])
        paper = self.by_id['karkideskilling2026']
        self.assertEqual(paper['doi'], '10.1515/humaff-2026-0080')
        self.assertEqual(paper['date'], '2026-09-23')
        self.assertEqual(paper['method'], 'empirically-informed-normative-argument')
        self.assertIn('self-report', paper['limitations'])
        self.assertIn('ref-712e3405f2', paper['related_to'])

    def test_artifact_identity_is_not_proof_verification(self):
        source = self.by_id['openaiunderstanding2026']
        self.assertEqual(source['title'], 'Working with academic communities to build scientific understanding')
        artifact = source['artifact_inspection']
        self.assertRegex(artifact['upstream_revision'], r'^[a-f0-9]{40}$')
        self.assertFalse(artifact['proofs_independently_checked'])
        self.assertRegex(artifact['manuscript_git_blob_sha'], r'^[a-f0-9]{40}$')
        for key in ['scope_note_url', 'manuscript_url']:
            self.assertIn(artifact['upstream_revision'], artifact[key])

    def test_buyout_reports_are_one_event_with_honest_access_scope(self):
        ids = ['stewartbuyouts2026', 'colemanexit2026', 'bishopbuyouts2026']
        self.assertEqual({self.by_id[key]['study_family'] for key in ids},
                         {'microsoft-voluntary-exit-october-2026'})
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        observations = {r['id']: r for r in ledger['observations']}
        self.assertFalse(observations['stewartbuyouts2026']['full_text_read'])
        for key in ['vandenbergagents2026', 'voytkoquality2026', 'karkideskilling2026']:
            self.assertTrue(observations[key]['full_text_read'])
        for key in ['stewartbuyouts2026', 'vandenbergagents2026', 'voytkoquality2026', 'karkideskilling2026']:
            self.assertIn(key, ledger['monthly_watchlist_additions_on_promotion'])

    def test_patching_case_preserves_period_and_mixed_cost_scope(self):
        source = self.by_id['sonpatching2026']
        self.assertEqual(source['authors'], ['Son, Hugh'])
        self.assertEqual(source['date'], '2026-10-14')
        scope = source['reported_measurement_scope']
        self.assertEqual(scope['contractors_added'], 1000)
        self.assertEqual(scope['contractor_addition_period'], '2026-Q2')
        self.assertEqual(scope['expense_period'], '2026-Q3')
        self.assertEqual(set(scope['expense_scope']),
                         {'software-remediation', 'anti-money-laundering-compliance'})
        for key in ['mythos_only_expense_established', 'net_ai_return_established',
                    'causal_employment_effect_established']:
            self.assertFalse(scope[key])
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        observation = next(r for r in ledger['observations'] if r['id'] == source['id'])
        self.assertTrue(observation['full_text_read'])
        self.assertIn(source['id'], ledger['monthly_watchlist_additions_on_promotion'])

    def test_security_advisories_have_stable_identifiers_and_families(self):
        self.assertIn('CVE-2026-109618', self.by_id['phpoom2026']['advisory_identifiers'])
        self.assertIn('CVE-2026-109619', self.by_id['phpstale2026']['advisory_identifiers'])
        for key in ['nodeoct2026', 'dotnetbrotli2026']:
            self.assertIn('CVE-2026-111497', self.by_id[key]['advisory_identifiers'])
            self.assertEqual(self.by_id[key]['study_family'], 'brotli-cve-2026-111497')
        for key in ['phpoom2026', 'phpstale2026', 'califphp2026', 'wizphp2026']:
            self.assertEqual(self.by_id[key]['study_family'], 'php2shell-2026')

    def test_security_snapshots_preserve_denominators_and_units(self):
        ledger = json.loads((ROOT / 'november/security-observations.json').read_text())
        self.assertEqual(ledger['target_release'], '2026-11')
        self.assertFalse(ledger['release_receipts_complete'])
        prevalence = ledger['w3techs_snapshot']
        self.assertEqual(prevalence['php_usage_percent'], 69.2)
        self.assertIn('known', prevalence['denominator'])
        self.assertFalse(prevalence['is_vulnerability_or_compromise_rate'])
        exposure = ledger['censys_snapshot']
        self.assertEqual(exposure['unit'], 'services')
        self.assertFalse(exposure['is_confirmed_compromise_count'])
        self.assertTrue(exposure['limitations'])
        for key in ['w3php2026', 'censysphp2026', 'cisakev2026']:
            self.assertTrue(self.by_id[key]['date_is_snapshot'])

    def test_known_exploitation_status_is_dated_not_global_sensor_absence(self):
        ledger = json.loads((ROOT / 'november/security-observations.json').read_text())
        snapshot = ledger['cisa_snapshot']
        dates = {r['cve_id']: r['date_added'] for r in snapshot['entries']}
        self.assertEqual(dates, {'CVE-2026-109618': '2026-10-26',
                                 'CVE-2026-109619': '2026-10-26',
                                 'CVE-2026-111497': '2026-10-27'})
        self.assertFalse(snapshot['establishes_attack_prevalence_or_attacker_ai_use'])
        for date in dates.values():
            self.assertLessEqual(date, ledger['checked_on'])
        self.assertLess(self.by_id['crowdphp2026']['date'], dates['CVE-2026-109618'])
        self.assertEqual(self.by_id['cisakev2026']['verification']['method'],
                         'official-machine-readable-feed')

    def test_security_dynamic_sources_have_browser_rechecks(self):
        ledger = json.loads((ROOT / 'november/browser-observations.json').read_text())
        observations = {r['id']: r for r in ledger['observations']}
        for key in ['wizphptel2026', 'w3php2026', 'censysphp2026']:
            self.assertIn(key, ledger['monthly_watchlist_additions_on_promotion'])
            self.assertEqual(observations[key]['inspection_date'], '2026-10-27')
            self.assertTrue(observations[key]['refresh_required'])

    def test_capability_evaluation_is_not_an_incident_count(self):
        ledger = json.loads((ROOT / 'november/security-observations.json').read_text())
        scope = ledger['anthropic_evaluation_scope']
        self.assertEqual(scope['firefox_engine_patches'], 18)
        self.assertEqual(scope['windows_local_privilege_escalation_patches'], 21)
        self.assertFalse(scope['independently_replicated_here'])
        self.assertFalse(scope['represents_observed_real_world_attacks'])

    def test_python_bindings_share_cve_without_inventing_api_metadata(self):
        ledger = json.loads((ROOT / 'november/security-observations.json').read_text())
        observation = ledger['python_package_observation']
        self.assertIsNone(observation['advisory_api_cve_id'])
        self.assertEqual(observation['shared_cve_mapping'], 'CVE-2026-111497')
        self.assertEqual({r['name']: r['fixed'] for r in observation['packages']},
                         {'brotli': '1.2.1', 'brotlicffi': '1.2.1.0'})
        self.assertTrue(observation['range_caveat'])
        self.assertFalse(observation['installation_alone_establishes_reachable_exposure'])
        self.assertFalse(observation['python_rce_independently_demonstrated_here'])
        self.assertFalse(observation['download_counts_are_exposure_counts'])
        for key in observation['source_ids']:
            self.assertEqual(self.by_id[key]['study_family'], 'brotli-cve-2026-111497')

    def test_python_source_publication_and_update_are_distinct(self):
        source = self.by_id['aikidopython2026']
        self.assertEqual(source['authors'], ['The Aikido Team'])
        self.assertEqual(source['date'], '2026-10-23')
        self.assertEqual(source['updated_date'], '2026-10-27')
        self.assertEqual(self.by_id['pythonbrotliadvisory2026']['date'], '2026-10-22')
