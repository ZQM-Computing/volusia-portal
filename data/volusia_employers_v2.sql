-- Volusia County Major Employers
-- SQLite-compatible schema + seed data.
-- Re-generated from database to sync with latest data

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS employers;
DROP TABLE IF EXISTS cities;
DROP TABLE IF EXISTS sectors;

CREATE TABLE sectors (
  sector_id   INTEGER PRIMARY KEY,
  name        TEXT NOT NULL UNIQUE,
  color       TEXT
);

CREATE TABLE cities (
  city_id     INTEGER PRIMARY KEY,
  name        TEXT NOT NULL UNIQUE,
  population_approx INTEGER
);

CREATE TABLE employers (
  employer_id INTEGER PRIMARY KEY,
  name        TEXT NOT NULL,
  sector_id   INTEGER NOT NULL REFERENCES sectors(sector_id),
  city_id     INTEGER NOT NULL REFERENCES cities(city_id),
  hq_in_volusia INTEGER DEFAULT 0,
  is_public   INTEGER DEFAULT 0,
  approx_employees INTEGER,
  avg_annual_wage_override INTEGER,
  description TEXT,
  keywords    TEXT,        -- space-delimited search tokens
  website     TEXT,
  source_verified_date TEXT
);

-- Enhanced schema with contact information
CREATE TABLE employers_extended AS SELECT * FROM (SELECT 1 as dummy LIMIT 0);

CREATE TABLE jobs (
  job_id      INTEGER PRIMARY KEY,
  employer_id INTEGER NOT NULL REFERENCES employers(employer_id),
  title       TEXT NOT NULL,
  family      TEXT,        -- e.g. Nursing, Engineering, Teaching
  remote_eligible INTEGER DEFAULT 0,
  entry_level INTEGER DEFAULT 0,
  posted_date TEXT,
  url         TEXT,
  source      TEXT
);

CREATE TABLE applications (
  app_id      INTEGER PRIMARY KEY,
  job_id      INTEGER NOT NULL REFERENCES jobs(job_id),
  applied_on  TEXT NOT NULL,
  status      TEXT DEFAULT 'submitted',
  notes       TEXT
);

-- Seed sectors
INSERT INTO sectors VALUES (1,'Healthcare & Life Sciences','#4CAF50');
INSERT INTO sectors VALUES (2,'Education','#2196F3');
INSERT INTO sectors VALUES (3,'Government & Public Safety','#FF9800');
INSERT INTO sectors VALUES (4,'Aviation / Aerospace','#00BCD4');
INSERT INTO sectors VALUES (5,'Insurance & Financial Services','#9C27B0');
INSERT INTO sectors VALUES (6,'Manufacturing','#607D8B');
INSERT INTO sectors VALUES (7,'Logistics & Distribution','#FF5722');
INSERT INTO sectors VALUES (8,'Retail','#8BC34A');
INSERT INTO sectors VALUES (9,'Hospitality & Entertainment','#E91E63');
INSERT INTO sectors VALUES (10,'Utilities & Infrastructure','#795548');
INSERT INTO sectors VALUES (11,'Construction','#FFC107');
INSERT INTO sectors VALUES (12,'Professional Services','#3F51B5');

-- Seed cities
INSERT INTO cities VALUES (1,'Daytona Beach',72000);
INSERT INTO cities VALUES (2,'DeLand',38000);
INSERT INTO cities VALUES (3,'Port Orange',65000);
INSERT INTO cities VALUES (4,'Deltona',90000);
INSERT INTO cities VALUES (5,'New Smyrna Beach',32000);
INSERT INTO cities VALUES (6,'Ormond Beach',45000);
INSERT INTO cities VALUES (7,'Edgewater',25000);
INSERT INTO cities VALUES (8,'Holly Hill',12000);
INSERT INTO cities VALUES (9,'Orange City',15000);
INSERT INTO cities VALUES (10,'DeLeon Springs',3000);
INSERT INTO cities VALUES (11,'Crystal River',4000);

-- 72 employers
-- (includes contact information)
-- Seed employers (public = government/education/coastal infrastructure)
INSERT INTO employers VALUES (1, 'Volusia County Schools', 2, 2, 0, 1, 8552, NULL, 'Largest employer in Volusia; 100+ schools; teachers/admin across all communities', 'education teaching k12 admin schools', 'https://www.vcs2.org', '2025-09-30', 'vcs_info@vcsedu.org', '386-734-7190', 'HR main line; Teacher Tuition Reimbursement office 386-822-6790');
INSERT INTO employers VALUES (2, 'AdventHealth Systems', 1, 2, 0, 0, 7198, NULL, 'Florida Hospital Volusia/Flagler network; acute care, cardiology, neurosciences, orthopedics', 'healthcare hospital nursing cardiology neurosciences orthopedics acute-care', 'https://www.adventhealth.com', '2025-09-30', 'https://www.adventhealth.com/careers', '407-303-1600', 'Central FL careers line; DeLand/Daytona campuses use same system');
INSERT INTO employers VALUES (3, 'Halifax Hospital System', 1, 1, 0, 0, 4811, NULL, '678-bed flagship; Level II trauma center for 90-mile coastal corridor; specialty clinics network', 'healthcare hospital trauma emergency physicians nursing', 'halifaxhealth.org/careers', '2025-09-30', 'careers@halifaxhealth.org', '386-425-4111', 'Careers portal; education assistance HR contact on file');
INSERT INTO employers VALUES (4, 'Publix Supermarkets', 8, 1, 0, 0, 4007, NULL, 'Employee-owned grocery chain; wide footprint across Volusia; strong management-development culture', 'retail grocery supermarket food pharmacy', 'https://www.publix.com', '2025-09-30', 'https://jobs.publix.com', '800-406-3444', 'Associate care / benefits inquiries; corporate Orlando region');
INSERT INTO employers VALUES (5, 'Walmart Associates', 8, 1, 0, 0, 3570, NULL, 'Supercenters across Daytona, Port Orange, DeLand, Deltona, NSB, Ormond Beach; store management pathways', 'retail big-box grocery general-merchandise', 'https://www.walmart.com', '2025-09-30', 'https://hiring.amazon.com', 'https://hiring.amazon.com', 'Walmart hiring center contact varies by store; Amazon Career Choice dedicated employer learning team');
INSERT INTO employers VALUES (6, 'Amazon', 7, 7, 0, 0, 3500, NULL, 'Edgewater fulfillment center on SR-442; 1M sq ft package operations; planned Deltona FC expansion', 'logistics fulfillment warehouse distribution supply-chain', 'amazon.jobs', '2025-09-30', 'hiring@amazon.com', '206-266-1000', 'Amazon corporate switchboard; Edgewater FC local HR via job portal');
INSERT INTO employers VALUES (7, 'County of Volusia', 3, 2, 0, 1, 2864, NULL, 'Countywide sheriff, utilities, transportation, public works; main admin campus in DeLand', 'government public-administration utilities transportation', 'https://www.volusia.org', '2025-09-30', 'https://www.volusia.org/jobs', '386-236-2000', 'County HR general line; job-related tuition reimbursement 386-736-5951 ext 13492');
INSERT INTO employers VALUES (8, 'State of Florida', 3, 2, 0, 1, 2773, NULL, 'Various Florida state agencies operating in Volusia County', 'government state agencies public', 'https://www.myflorida.com', '2025-09-30', 'Careers@dos.myflorida.com', '850-487-1220', 'State HR main line; FRS retirement administered through MyFloridaHR');
INSERT INTO employers VALUES (9, 'Brown & Brown Insurance', 5, 1, 1, 0, 3500, NULL, 'Fortune 500 brokerage HQ on Beach Street; wholesale, specialty programs, risk-consulting subsidiaries', 'insurance brokerage commercial risk-management financial-services fortune-500', 'us.bbrown.com/careers', '2025-09-30', 'talent@bbrown.com', '386-255-6500', 'Daytona Beach HQ main line; careers inbox via website');
INSERT INTO employers VALUES (10, 'Embry-Riddle Aeronautical University', 4, 1, 1, 0, 1992, NULL, 'World-premier aviation/aerospace university; programs in aeronautical science, aerospace engineering, ATC', 'aviation aerospace education flight-training research university', 'careers.erau.edu', '2025-09-30', 'careers@erau.edu', '386-226-6000', 'Daytona Beach campus HR line');
INSERT INTO employers VALUES (11, 'Stetson University', 2, 2, 1, 0, 1446, NULL, 'Florida oldest private university; DeLand campus; law/business grad programs in Gulfport', 'education university law business liberal-arts', 'stetson.edu/hr', '2025-09-30', 'hr@stetson.edu', '386-822-7100', 'HR admin line; academic and staff roles');
INSERT INTO employers VALUES (12, 'Daytona State College', 2, 1, 0, 0, 1414, NULL, 'Primary access institution; ISB main campus; branches DeLand, NSB, Deltona, Flagler/Palm Coast', 'education community-college workforce technical', 'daytonastate.edu/hr', '2025-09-30', 'hr@daytonastate.edu', '386-506-4505', 'Human Resources main line; benefits and tuition reimbursement inquiries');
INSERT INTO employers VALUES (13, 'City of Daytona Beach', 3, 1, 0, 1, 1026, NULL, 'Police, fire, public works, planning; downtown revitalization active', 'government municipal police fire public-works', 'codajobs.com', '2025-09-30', 'HR@codajobs.com', '386-671-3000', 'City HR; NeoGov/CODA job board is official application portal');
INSERT INTO employers VALUES (14, 'Volusia County Sheriff''s Office', 3, 2, 0, 1, 875, NULL, 'Regional law enforcement; patrol, investigation, detention, civil process', 'government law-enforcement sheriff public-safety', 'https://www.volusiasheriff.org', '2025-09-30', NULL, NULL, NULL);
INSERT INTO employers VALUES (15, 'Florida Healthcare Plans', 1, 8, 0, 0, 972, NULL, 'Holly Hill; managed care/HMO operations', 'healthcare insurance managed-care hmo', 'https://www.floridahealthcareplans.com', '2025-09-30', 'https://www.floridahealthcareplans.com', '386-236-2012', 'Local health-plan HR; Daytona-area plan admin roles');
INSERT INTO employers VALUES (16, 'Bethune-Cookman University', 2, 1, 1, 0, 900, NULL, 'Historically Black university founded by Mary McLeod Bethune; education/social-equity mission', 'education historically-black university hbcu', 'cookman.edu/hr', '2025-09-30', 'hr@cookman.edu', '386-481-2000', 'HR main line; faculty/staff openings');
INSERT INTO employers VALUES (17, 'Duke Energy Florida', 10, 2, 0, 0, 900, NULL, 'Transmission infrastructure, substations, customer service across coastal NE FL', 'utilities energy power transmission electrical', 'https://www.duke-energy.com', '2025-09-30', 'careerteam@duke-energy.com', '800-228-8480', 'Candidate care line; tuition reimbursement via ETAP portal');
INSERT INTO employers VALUES (18, 'Boston Whaler / Brunswick Corporation', 6, 7, 1, 0, 736, NULL, 'Edgewater; premium fiberglass sport/fishing boats; marine manufacturing', 'manufacturing marine boats fiberglass boat-building', 'https://www.brunswick.com', '2025-09-30', 'healthcareers@brunswick.com', '800-633-8222', 'Brunswick corporate HR; Edgewater plant staffing via local EDC');
INSERT INTO employers VALUES (19, 'U.S. Government', 3, 2, 0, 1, 736, NULL, 'Federal operations, agencies, contract workforce in Volusia County', 'government federal military contracts', 'https://www.usa.gov', '2025-09-30', 'https://www.usajobs.gov', '1-866-606-8220', 'USAJobs help desk; federal benefits through OPM');
INSERT INTO employers VALUES (20, 'U.S. Postal Service', 7, 2, 0, 1, 721, NULL, 'Mail processing and retail units serving Volusia County', 'logistics mail postal distribution', 'https://www.usps.com', '2025-09-30', 'https://www.usps.com/careers', '800-333-1825', 'National HR; local Daytona/Volusia openings via USAJobs');
INSERT INTO employers VALUES (21, 'Sparton Electronics', 6, 10, 0, 0, 460, NULL, 'DeLeon Springs; electronics and defense/aerospace component manufacturing', 'manufacturing electronics defense aerospace-components', 'https://www.sparton.com', '2025-09-30', 'https://www.sparton.com', '586-243-6800', 'Corporate HR; local plant contact via public switchboard');
INSERT INTO employers VALUES (22, 'Teledyne Marine / Teledyne Oil and Gas', 6, 1, 0, 0, 525, NULL, 'Daytona Beach; precision instrumentation for marine, undersea, and industrial markets', 'manufacturing marine instrumentation undersea oil-gas sensors', 'https://www.teledyne.com', '2025-09-30', 'https://www.teledyne.com/careers', '805-373-4400', 'Corporate HR; marine tech roles posted company-wide');
INSERT INTO employers VALUES (23, 'Frontier Communications', 6, 2, 0, 0, 500, NULL, 'DeLand HQ; telecom/connectivity provider', 'telecommunications internet fiber connectivity isp', 'https://www.frontier.com', '2025-09-30', 'https://www.frontier.com/careers', '800-921-8101', 'HR line; Florida operations hiring through regional postings');
INSERT INTO employers VALUES (24, 'U.S. Foods', 7, 5, 0, 0, 500, NULL, 'Port Orange; regional foodservice distribution to restaurants/institutions', 'logistics foodservice distribution wholesale', 'https://www.usfoods.com', '2025-09-30', 'https://careers.usfoods.com', '800-477-3820', 'Distribution operations HR; Daytona hub openings via careers portal');
INSERT INTO employers VALUES (25, 'World Class Distribution / Trader Joe''s', 7, 1, 0, 0, 450, NULL, 'Daytona Beach; regional distribution center for Trader Joe''s private-label groceries', 'logistics grocery distribution retail', 'https://www.ziprecruiter.com', '2025-09-30', 'careers@ziprecruiter.com', NULL, NULL);
INSERT INTO employers VALUES (26, 'Brown & Brown Subsidiary Operations', 5, 1, 0, 0, 500, NULL, 'Wholesale brokerage, specialty programs, risk-management consulting divisions in Daytona Beach', 'insurance brokerage risk-management consulting', 'https://www.bbinsurance.com', '2025-09-30', 'https://us.bbrown.com/careers', '386-255-6500', 'Shared Daytona HQ contact for subsidiary temp/contract pools');
INSERT INTO employers VALUES (27, 'Halifax Health Trauma / Specialty Clinics', 1, 1, 0, 0, 500, NULL, 'Port Orange / Ormond Beach / New Smyrna Beach; high-acuity trauma and specialty-network expansion', 'healthcare trauma emergency specialty-clinics', 'https://www.halifaxhealth.org', '2025-09-30', NULL, NULL, NULL);
INSERT INTO employers VALUES (28, 'ICI Homes (Mori Hosseini Companies)', 11, 1, 1, 0, 800, NULL, 'Florida largest private homebuilder; active communities NE/Central FL; construction/project management workforce', 'construction homebuilding residential real-estate development', 'https://www.icihomes.com', '2025-09-30', 'https://www.icihomes.com', '386-258-6700', 'Daytona Beach HQ; careers page directs to HR intake form');
INSERT INTO employers VALUES (29, 'Daytona Beach International Airport', 10, 1, 0, 1, 500, NULL, 'Air traffic control, TSA, maintenance, authority administration; supports Embry-Riddle flight ops', 'aviation airport transportation logistics', 'https://www.flydaytonabeach.com', '2025-09-30', 'https://www.flydaytonafirst.com', '386-873-0490', 'Airport HR line; public-safety/ops roles posted separately');
INSERT INTO employers VALUES (30, 'Lowe''s', 8, 2, 0, 0, 600, NULL, 'Building materials/home improvement stores across Volusia; pro desk, department management', 'retail home-improvement building-materials', 'https://careers.lowes.com', '2025-09-30', 'careers@corporate.lowes.com', NULL, NULL);
INSERT INTO employers VALUES (31, 'Publix Super Markets', 8, 3, 0, 0, 900, NULL, 'Separate grocery management/distribution footprint; leadership development across coastal/inland stores', 'retail grocery management distribution', 'https://jobs.publix.com', '2025-09-30', 'careers@publixtalent.com', '800-406-3444', NULL);
INSERT INTO employers VALUES (32, 'FedEx Ground Daytona Hub', 7, 1, 0, 0, 500, NULL, 'Daytona Beach hub processing Volusia/Flagler shipments; package handlers, linehaul drivers', 'logistics shipping hub package delivery', 'https://www.fedex.com/careers', '2025-09-30', 'careers@fedex.com', '800-463-3339', NULL);
INSERT INTO employers VALUES (33, 'Home Depot', 8, 2, 0, 0, 550, NULL, 'Daytona, Port Orange, DeLand, Deltona; pro desk, department supervisors', 'retail home-improvement contractor tools', 'https://corporate.homedepot.com/careers', '2025-09-30', 'careers@homedepot.com', NULL, NULL);
INSERT INTO employers VALUES (34, 'Target', 8, 1, 0, 0, 450, NULL, 'Daytona Beach and Port Orange stores; general merchandise, grocery, style/brand-forward hiring', 'retail general-merchandise style grocery', 'https://corporate.target.com/careers', '2025-09-30', 'careers@corporate.target.com', NULL, NULL);
INSERT INTO employers VALUES (35, 'Rooms To Go Regional Distribution', 8, 1, 0, 0, 400, NULL, 'Daytona industrial corridor furniture distribution/delivery across NE FL and Space Coast', 'retail furniture distribution warehouse delivery', 'https://www.roomstogo.com', '2025-09-30', 'https://www.joinrooms2go.com/en/careers.html', '813-555-7000', 'Corporate HR; temp shift inquiries often through local staffing partners');
INSERT INTO employers VALUES (36, 'B. Braun Medical Inc.', 1, 1, 0, 0, 175, NULL, 'Daytona Beach; IV solutions, infusion therapy, medical devices; Fortune 500-adjacent manufacturer', 'healthcare manufacturing medical-devices iv-infusion pharma', 'https://www.bbraunusa.com', '2025-09-30', 'https://www.bbraun.com/careers', '800-456-9000', 'Corporate HR; US medical devices benefits line');
INSERT INTO employers VALUES (37, 'Aerojet Rocketdyne 3DMT', 4, 1, 0, 0, NULL, NULL, 'Daytona Beach; aerospace propulsion and defense manufacturing', 'aerospace defense propulsion propulsion-components rocket', 'https://www.aerojetrocketdyne.com', '2025-09-30', 'https://www.rocket.com/careers', '916-355-4000', 'Corporate HR; Daytona-area defense manufacturing roles');
INSERT INTO employers VALUES (38, 'Embry-Riddle CATER / Research Parks', 4, 1, 0, 0, 300, NULL, 'Center for Aviation, Transportation, and the Environment; NASA, FAA, defense contracts', 'aviation aerospace research engineering defense-contracts', 'https://www.erau.edu', '2025-09-30', NULL, NULL, NULL);
INSERT INTO employers VALUES (39, 'NASCAR / International Speedway Corp.', 9, 1, 1, 0, 760, NULL, 'Global HQ and Daytona International Speedway; engineering, broadcast, event operations; Daytona Rising 2016', 'hospitality motorsports racing sports entertainment events', 'https://www.nascar.com', '2025-09-30', 'https://www.nascar.com/careers', '904-633-6100', 'Daytona Beach corporate HR; event roles via seasonal job boards');
INSERT INTO employers VALUES (40, 'Florida Power & Light', 10, 1, 0, 0, 300, NULL, 'Daytona Beach service center; coastal corridor line crews/substation/CSR from Holly Hill to Edgewater', 'utilities electrical power solar infrastructure', 'https://www.fpl.com', '2025-09-30', 'recruiting.daytona@fpl.com', '561-694-4000', 'See also Duke Energy; benefits aligned through NextEra/FP&L stack');
INSERT INTO employers VALUES (41, 'Everglades Boats', 6, 7, 0, 0, 189, NULL, 'Edgewater; high-performance bay and flats boats', 'manufacturing marine boats performance-fishing', 'https://www.evergladesboats.com', '2025-09-30', 'https://www.evergladesboats.com', 'https://www.evergladesboats.com', 'Contact via website dealer/careers page');
INSERT INTO employers VALUES (42, 'EdgeWater Power Boats', 6, 7, 0, 0, 105, NULL, 'Edgewater; family fishing boats; fiberglass construction', 'manufacturing marine boats fiberglass', 'https://www.edgewaterboats.com', '2025-09-30', 'https://www.edgewaterboats.com', 'https://www.edgewaterboats.com', 'Contact via website careers page');
INSERT INTO employers VALUES (44, 'DaVita Labs', 1, 2, 0, 0, 300, NULL, 'DeLand; laboratory/dialysis services operations', 'healthcare laboratory dialysis kidney', 'https://www.davita.com', '2025-09-30', 'https://www.davita.com/careers', '773-486-4000', 'National renal care HR; DeLand center roles');
INSERT INTO employers VALUES (45, 'Medtronic', 1, 2, 0, 0, 525, NULL, 'DeLand presence; medical device manufacturing/distribution', 'healthcare manufacturing medical-devices medtech', 'https://www.medtronic.com', '2025-09-30', 'https://www.medtronic.com/careers', '800-328-2510', 'DeLand/NE FL roles through global portal');
INSERT INTO employers VALUES (46, 'Truist / SunTrust Volusia', 5, 1, 0, 0, 350, NULL, 'Branches, mortgage origination, commercial lending across coastal/inland markets', 'banking mortgage commercial lending financial', 'https://www.truist.com', '2025-09-30', 'https://www.truist.com/careers', '855-628-8468', 'Candidate contact center; local branches manage hybrid role eligibility');
INSERT INTO employers VALUES (47, 'Dougherty Manufacturing', 6, 2, 0, 0, NULL, NULL, 'Southeast Volusia; machining/fabrication manufacturer', 'manufacturing machining fabrication metal', 'https://www.ziprecruiter.com', NULL, 'careers@doughertymfg.com', '', 'Temp employer contact via ZipRecruiter/Staffing partners');
INSERT INTO employers VALUES (48, 'Blue Water Dynamics', 4, 7, 0, 0, NULL, NULL, 'Edgewater area; marine/aerospace systems components', 'aerospace marine dynamics components', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local postings through staffing partners');
INSERT INTO employers VALUES (49, 'Sauer Southeast / Sauer Group', 4, 6, 0, 0, NULL, NULL, 'Ormond Beach area; aviation power systems supplier', 'aviation hydraulic power aerospace', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local postings through staffing partners');
INSERT INTO employers VALUES (50, 'Power Flow Systems', 4, 5, 0, 0, NULL, NULL, 'New Smyrna Beach area; aerospace flow components', 'aerospace flow-components propulsion', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local postings through staffing partners');
INSERT INTO employers VALUES (51, 'Cardinal Health', 1, 1, 0, 0, NULL, NULL, 'Daytona Beach area presence; medical/surgical products distribution and mfg', 'healthcare medical surgical distribution medtech', 'cardinalhealth.com', '2025-09-30', 'cardinalhealth@att.net', '614-225-2000', 'Corporate HR; medical/surgical logistics roles');
INSERT INTO employers VALUES (52, 'Command Medical Products', 1, 2, 0, 0, NULL, NULL, 'DeLand / Volusia area; wound/surgical product manufacturing', 'healthcare manufacturing surgical wound-care', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local postings through staffing partners');
INSERT INTO employers VALUES (53, 'CEMEX Construction Materials Florida', 6, 5, 0, 0, NULL, NULL, 'New Smyrna Beach; aggregates, cement, ready-mix concrete', 'construction aggregates cement concrete building-materials', 'https://www.cemex.com', '2025-09-30', 'https://www.cemexusa.com', '877-236-8527', 'Corporate contact; FL materials/plant operations openings');
INSERT INTO employers VALUES (54, 'Momentive Performance Materials', 6, 2, 0, 0, NULL, NULL, 'DeLand area; specialty chemicals, silicone, quartz materials', 'manufacturing chemicals silicone materials specialty', 'https://www.momentive.com', '2025-09-30', 'https://www.momentive.com', 'https://www.momentive.com', 'Careers page; global HR lines for Albany NY HQ');
INSERT INTO employers VALUES (55, 'Porta Products Corporation', 6, 7, 0, 0, NULL, NULL, 'Edgewater; fiberglass/composite product manufacturing', 'manufacturing composites fiberglass products marine', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local postings through staffing partners');
INSERT INTO employers VALUES (56, 'Custom Tube Products', 6, 2, 0, 0, NULL, NULL, 'DeLand; custom metal tube fabrication and laser-cutting', 'manufacturing metal fabrication laser-cutting tubing', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (57, 'Schultz Engineered Products', 6, 2, 0, 0, NULL, NULL, 'DeLand; engineered fabricated metal components', 'manufacturing metal fabrication engineered-components', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (58, 'Titan Florida', 6, 2, 0, 0, NULL, NULL, 'DeLand area; metal stamping/fabrication for OEMs', 'manufacturing metal stamping fabrication oem', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (59, 'Steward Performance Products', 6, 2, 0, 0, NULL, NULL, 'Volusia area; specialty performance materials', 'manufacturing materials specialty chemicals', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (60, 'Advanced Machining Inc', 6, 2, 0, 0, NULL, NULL, 'West Volusia area; CNC machining and job-shop manufacturing', 'manufacturing machining cnc job-shop', 'https://www.ziprecruiter.com', NULL, 'careers@advancedmachiningfl.com', '', 'Temp employer contact via ZipRecruiter/American Staffing partners');
INSERT INTO employers VALUES (61, 'Mil Spec Metal Finishing', 6, 7, 0, 0, NULL, NULL, 'Edgewater; anodizing/plating for defense and aerospace', 'manufacturing metal-finishing aerospace defense', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (62, 'American Awning & Ornamental Aluminum', 6, 5, 0, 0, NULL, NULL, 'New Smyrna Beach; awnings, aluminum fabrication', 'manufacturing aluminum fabrication awnings', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (63, 'E-Sector Machining and Fabrication', 6, 7, 0, 0, NULL, NULL, 'Edgewater; precision machining/welding/fabrication', 'manufacturing machining welding fabrication precision', '', NULL, NULL, NULL, NULL);
INSERT INTO employers VALUES (64, 'Advanced Weapons & Firearms LLC', 6, 5, 0, 0, NULL, NULL, 'New Smyrna Beach; firearms/manufacturing small arms components', 'manufacturing firearms components precision', '', NULL, NULL, NULL, NULL);
INSERT INTO employers VALUES (65, 'Allied International Corporation', 6, 3, 0, 0, NULL, NULL, 'Port Orange; heavier industrial supply/remanufacturing', 'manufacturing remanufacturing industrial supply', '', NULL, NULL, NULL, NULL);
INSERT INTO employers VALUES (66, 'Goss Inc', 6, 2, 0, 0, NULL, NULL, 'DeLand area; engineered marine products/hatches', 'manufacturing marine products engineered', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (67, 'Blue Coast Bakers', 1, 3, 0, 0, 300, NULL, 'Port Orange; baked-goods/food manufacturing', 'food manufacturing baking retail', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (68, 'Kennel Master Foods', 1, 5, 0, 0, NULL, NULL, 'New Smyrna Beach area; pet food manufacturing', 'manufacturing petfood food', '', NULL, 'https://www.ziprecruiter.com', 'https://www.ziprecruiter.com', 'Local job postings through staffing partners');
INSERT INTO employers VALUES (69, 'Foundation Risk Partners', 5, 1, 0, 0, NULL, NULL, 'Daytona Beach area; insurance/risk-management brokerage', 'insurance brokerage risk-management financial', 'foundationrp.com', '2025-09-30', 'info@foundationrp.com', '', 'Apply via LinkedIn or company careers page');
INSERT INTO employers VALUES (70, 'Security First Insurance', 5, 1, 1, 0, NULL, NULL, 'Daytona Beach HQ or near-county; Florida property/casualty', 'insurance property-casualty homeowner florida', 'https://www.securityfirstinsurance.com', '2025-09-30', 'https://www.securityfirstflorida.com/careers', '386-734-7200', 'Ormond/Daytona operations contact line');
INSERT INTO employers VALUES (71, 'TopBuild', 11, 1, 1, 0, NULL, NULL, 'Daytona Beach HQ; insulation installation/building products', 'construction insulation building-products installation', 'https://www.topbuild.com', '2025-09-30', 'https://www.topbuild.com/careers', '239-489-9400', 'Corporate HR; construction franchise roles');
INSERT INTO employers VALUES (72, 'Kingspan Insulated Panels', 6, 2, 1, 0, 144, NULL, 'DeLand HQ/operations; insulated metal panels/building envelopes', 'manufacturing insulated-panels building-envelope', 'https://www.kingspan.com', '2025-09-30', 'https://www.kingspan.com', 'https://www.kingspan.com', 'Apply via company careers site');
INSERT INTO employers VALUES (73, 'Cardinal Health Medical/Surgical', 1, 1, 0, 0, NULL, NULL, 'Daytona Beach area; surgical/medical products manufacturing distribution', 'healthcare manufacturing medical surgical', 'https://www.cardinalhealth.com', '2025-09-30', 'https://www.cardinalhealth.com/careers', '614-225-2000', 'Shared Cardinal Health contact; medical/surgical operations');

-- 29 jobs
-- Seed representative jobs
INSERT INTO jobs VALUES (64, 2, 'Registered Nurse - Med Surg', 'Nursing', 1, 0, '2026-07-15', 'https://careers.adventhealth.com', 'AdventHealth');
INSERT INTO jobs VALUES (65, 2, 'Nurse Tech - Student RN', 'Nursing', 0, 1, '2026-07-12', 'https://careers.adventhealth.com/nurse-tech-jobs', 'AdventHealth');
INSERT INTO jobs VALUES (66, 3, 'Registered Nurse ICU', 'Nursing', 0, 0, '2026-07-10', 'https://halifaxhealth.org/careers', 'Halifax');
INSERT INTO jobs VALUES (67, 3, 'Clinical Lab Scientist', 'Laboratory', 0, 0, '2026-07-09', 'https://halifaxhealth.org/careers', 'Halifax');
INSERT INTO jobs VALUES (68, 27, 'Trauma Registrar', 'Health Information', 0, 0, '2026-07-11', 'https://halifaxhealth.org/careers', 'Halifax Specialty');
INSERT INTO jobs VALUES (69, 6, 'GIS Technician - Environmental Review', 'Geospatial', 1, 0, '2026-07-08', 'https://www.amazon.jobs', 'Amazon');
INSERT INTO jobs VALUES (70, 7, 'GIS Specialist - Public Works', 'Geospatial', 1, 0, '2026-07-14', 'https://www.volusia.org', 'Volusia County Government');
INSERT INTO jobs VALUES (71, 7, 'Engineering Inspector', 'Infrastructure', 0, 0, '2026-07-13', 'https://www.volusia.org', 'Volusia County Government');
INSERT INTO jobs VALUES (72, 8, 'Geographic Data Analyst - District', 'Geospatial', 1, 0, '2026-07-07', 'https://www.myfloridacareers.com', 'State of Florida');
INSERT INTO jobs VALUES (73, 12, 'GIS Adjunct Instructor', 'Education', 0, 1, '2026-07-06', 'https://daytonastate.edu/faculty-staff/hr/careers', 'Daytona State College');
INSERT INTO jobs VALUES (74, 13, 'Planning/GIS Analyst', 'Planning', 1, 0, '2026-07-16', 'https://www.codajobs.com', 'City of Daytona Beach');
INSERT INTO jobs VALUES (75, 38, 'Geospatial Analyst - Research', 'Geospatial', 1, 0, '2026-07-08', 'https://careers.erau.edu', 'Embry-Riddle CATER');
INSERT INTO jobs VALUES (76, 9, 'Risk Analyst - Coastal Exposure', 'Insurance', 1, 0, '2026-07-15', 'https://us.bbrown.com/careers', 'Brown & Brown');
INSERT INTO jobs VALUES (77, 9, 'Commercial Lines Customer Success', 'Insurance', 1, 0, '2026-07-14', 'https://us.bbrown.com/careers', 'Brown & Brown');
INSERT INTO jobs VALUES (78, 46, 'Credit Risk Analyst', 'Banking', 1, 0, '2026-07-10', 'https://www.truist.com', 'Truist Volusia');
INSERT INTO jobs VALUES (79, 69, 'Data Analyst - Claims', 'Insurance', 1, 0, '2026-07-12', 'https://www.foundationrp.com', 'Foundation Risk Partners');
INSERT INTO jobs VALUES (80, 70, 'Underwriting Operations', 'Insurance', 1, 0, '2026-07-11', 'https://www.securityfirstflorida.com/careers', 'Security First Insurance');
INSERT INTO jobs VALUES (81, 4, 'Pharmacy Clerk / Cashier', 'Retail', 0, 1, '2026-07-18', 'https://jobs.publix.com', 'Publix');
INSERT INTO jobs VALUES (82, 5, 'Fulfillment Associate', 'Logistics', 0, 1, '2026-07-17', 'https://hiring.amazon.com', 'Amazon Edgewater');
INSERT INTO jobs VALUES (83, 25, 'Picker/Packer - Temp Pool', 'Warehouse', 0, 1, '2026-07-16', 'https://www.ziprecruiter.com', 'World Class Distribution / Trader Joe’s');
INSERT INTO jobs VALUES (84, 30, 'Customer Service Associate', 'Retail', 0, 1, '2026-07-18', 'https://careers.lowes.com', 'Lowe’s Daytona');
INSERT INTO jobs VALUES (85, 31, 'Online Order Sorter', 'Grocery Fulfillment', 0, 1, '2026-07-17', 'https://jobs.publix.com', 'Publix Instacart/Online');
INSERT INTO jobs VALUES (86, 32, 'Package Handler - Hub', 'Logistics', 0, 1, '2026-07-17', 'https://www.fedex.com', 'FedEx Ground Daytona');
INSERT INTO jobs VALUES (87, 33, 'Sales Associate', 'Retail', 0, 1, '2026-07-18', 'https://corporate.homedepot.com', 'Home Depot');
INSERT INTO jobs VALUES (88, 34, 'Cashier / Front End', 'Retail', 0, 1, '2026-07-19', 'https://corporate.target.com', 'Target');
INSERT INTO jobs VALUES (89, 26, 'Administrative Temporary - Daytona', 'Administrative', 1, 1, '2026-07-19', 'https://www.ziprecruiter.com', 'Brown & Brown Subsidiary Operations');
INSERT INTO jobs VALUES (90, 47, 'General Labor - Machine Shop', 'Skilled Trades', 0, 1, '2026-07-14', 'https://www.ziprecruiter.com', 'Dougherty Manufacturing');
INSERT INTO jobs VALUES (91, 60, 'CNC Operator Temporary', 'Manufacturing', 0, 1, '2026-07-15', 'https://www.ziprecruiter.com', 'Advanced Machining Inc');
INSERT INTO jobs VALUES (92, 35, 'Warehouse Sort - Temp', 'Warehouse', 0, 1, '2026-07-16', 'https://jooble.org', 'Rooms To Go Regional Distribution');