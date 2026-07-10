from pipelineFramework import Configuration, LocalisationString

TECHNOLOGIES_CONFIG = Configuration(
    "fwf_query",
    LocalisationString("FWF Query Transform", "FWF Query Transformation"),
    [
        {"column": "externalId", "name": "id"},
        {"column": "uri", "name": "_str.uri"},
        {"column": "title", "name": "_str.projecttitle.de"},
        {"column": "grant", "name": "_str.grantdoi"},
        {"column": "start", "name": "_date.startdate"},
        {"column": "end", "name": "_date.enddate"},
        {"column": "status", "name": "_str.status.en"},
        {
            "column": "keywords",
            "concat": [
                "_list.researchareas.de",
                "_list.researchfields.de",
                "_list.researchdisciplines.de",
                "list.keywords.split",
            ],
        },
        {
            "column": "organisations",
            "concat": [
                "_list.researchinstitutes",
                "_list.nationalprojectparticipants.de",
                "_list.internationalprojectparticipants.de",
            ],
            "objectName": "rawString",
            "indexName": ["research", "national", "international"],
        },
        {"column": "abstract", "concat": ["_str.prproposalsummary.de", "_str.prfinalreport.de"]},
    ],
)
