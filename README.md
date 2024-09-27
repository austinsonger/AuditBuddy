# AuditBuddy [Not Production Ready] 

This GitHub Action automates evidence collection for compliance frameworks like SOC 2, ISO 27001, FedRAMP, and PCI DSS. It integrates with various cloud providers (AWS, Azure, GCP) and security tools (Okta, Tenable, etc.) to extract relevant data based on the chosen framework and control. The collected evidence is then formatted and committed to a designated location within the user's GitHub repository, simplifying compliance audits.

- [Evidence Collection](#evidence-collection)
- [Framework Requirements](#framework-requirements)
- [Language and Configuration Files](#language-and-configuration-files)
- [Integration with Cloud Providers and Security Tools](#integration-with-cloud-providers-and-security-tools)
- [Evidence Collection Logic](#evidence-collection-logic)
- [Commit and Push Evidence](#commit-and-push-evidence)


## Framework Requirements:

* Framework Specificity: 
    * Each framework has control objectives and corresponding controls with evidence types (e.g., policies, procedures, logs).
* Mapping Framework Controls to Evidence: 
    * Create a mapping between specific framework controls and the type of evidence they require (e.g., Population for user access controls, Configurations for security settings).

## Language and Configuration Files
- Python
- `YAML`
- `json`

## Integration with Cloud Providers and Security Tools

* SDKs and APIs: 
    * Utilize the official SDKs or APIs provided by each cloud provider (AWS, Azure, GCP) and security tool (Okta, OneLogin, Tenable, Elastic, Splunk, CrowdStrike) to interact with them. This will allow you to pull relevant evidence based on the framework and control being assessed.
        * https://aws.amazon.com/sdk-for-python/
        * https://github.com/Azure/azure-sdk-for-python
        * https://github.com/googleapis/google-cloud-python
        * https://github.com/okta/okta-sdk-python
        * https://pypi.org/project/elasticsearch/
        * https://github.com/CrowdStrike/falconpy
        * https://github.com/splunk/splunk-sdk-python
        * https://github.com/TheJumpCloud/jcapi-python
        * https://github.com/onelogin/onelogin-python-sdk
        * https://github.com/tenable/pyTenable
        * https://github.com/onelogin/onelogin-python-sdk
* Authentication: 
    * Implement secure authentication methods (e.g., OAuth, API keys) to connect with each platform. Store these credentials securely within the Github Action workflow using secrets.

## Evidence Collection Logic

* Framework Selection: 
    * Allow users to specify the framework they're targeting within the Github Action workflow.
* Control Mapping: 
    * Based on the chosen framework and control being assessed, use the mapping created earlier to identify the type of evidence needed.
* Data Extraction: 
    * Leverage the SDKs/APIs to extract relevant data from each cloud provider and security tool based on the control objective.
* Data Formatting: 
    * Format the extracted data according to your defined structure (Populations, Configurations, Rules, Samples).

## Commit and Push Evidence
* Version Control: 
    * Use Git commands within the Github Action workflow to commit the collected evidence files to a dedicated branch.
* Push Automation
    * Configure the workflow to automatically push the committed evidence to the desired location in the repository.

## Evidence Collection

### Tools
- [ ] Amazon Web Services
- [ ] Atlassian
- [ ] Okta
- [ ] Jumpcloud
- [ ] Tenable
- [ ] SentinelOne
- [ ] Splunk
- [ ] Cloudflare

#### Roadmap
- [Roadmap for future tools](https://github.com/austinsonger/Evidence-and-POAM-Generation/issues?q=is%3Aopen+is%3Aissue+label%3AROADMAP)


### Evidence Mapping

- [ ] - Private Sector
- [ ] - Federal

#### Federal

| Frequency | Auditor  Evidence ID # | Evidence                                                     | Github Action                                         | Evidence Output                                    | FedRAMP Mapping               | NIST Mapping |
| --------- | ---------------------- | ------------------------------------------------------------ | ----------------------------------------------------- | -------------------------------------------------- | :------------------------- | ------------ |
|           |                        |                                                              |                                                       |                                                    |                            |              |
|           |                        |                                                              |                                                       |                                                    |                            |              |

#### Private Sector

| Frequency | Auditor  Evidence ID # | Evidence                                                     | Github Action                                         | Evidence Output                                    | SOC2 Mapping               | NIST Mapping |
| --------- | ---------------------- | ------------------------------------------------------------ | ----------------------------------------------------- | -------------------------------------------------- | :------------------------- | ------------ |
|           |                        |                                                              |                                                       |                                                    |                            |              |
|           |                        |                                                              |                                                       |                                                    |                            |              |

