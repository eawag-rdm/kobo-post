# kobopost

## Summary

Package to post-process surveys that were created with [kobotoolbox](http://www.kobotoolbox.org).

Currently this provides one command line script: **`mark_skipped`**.

Kobotoolbox provides applications and a platform to design and apply surveys. Among other features, kobotoolbox allows conditional questions, that is questions that are skipped if a condition (usually referring to previous questions) is not met. Also **`kobopost`** allows to create groups of questions, which, among other uses, can be repeated in a loop.**`kobopost`** addresses two shortcomings:

1. Conditional questions that were skipped are indistinguishable from questions that were asked but did not get an answer. This is very unsatisfying when it comes to analysis.

2. Grouped questions of a survey are recorded in different worksheets from the other questions in the resulting workbook. Combining them can be a non-trivial business.

## Usage

`mark_skipped <questionaire> <form_definition> <outpath>`

Processes \<questionaire\>, an xlsx-file, based on \<form_definition\>, an xls file,
and writes the output to an appropriately named file in \<outpath\>.

## Output

+ Questions that were identified as "skipped" by the form-definition have the value **`_SKIPPED_`**.
+ Other questions with "empty" content get the value **`NA`**, as this is the most common and least problematic way to represent missing values (see [Jonathan Callahan's treatise](http://mazamascience.com/WorkingWithData/?p=343)).
+ The output-file is an [RFC4180](https://www.ietf.org/rfc/rfc4180.txt) conforming CSV file, UTF-8 encoded, with comma as field separator and `\r\n` as line-ending.
+ "Group questions" have column header `group_<XXXXX>[<i>]/<question>`, where `<XXXXX>` is the group descriptor, `<i>` is the loop iteration and `<question>` is the question descriptor.

## Installation

`pip install git+https://github.com/eawag-rdm/kobo-post.git`

### Requirements

+ Python 3
+ The survey data should have been downloaded from [kc.kobotoolbox.org](https://kc.kobotoolbox.org) with the following steps:    
`Projects` -> \<Project Name\> -> `Download data` -> `XLS` -> `Advanced Export` -> [Delimiter = "/"; check "DONT split select multiple choice answers into separate columns"] -> `Create Export`.
+ The form-definition should have been downloaded as:   
`Projects` -> \<Project Name\> -> [Download Symbol under heading "Form"] -> `XLS`.

## Caveats

+ The form definition language ([XLSForm](http://xlsform.org/)) seems quite powerful. Not all features are likely implemented because the documentation for XLSForm is incomplete. If you run into such a problem please raise an [Issue](https://github.com/eawag-rdm/koboforms/issues), I'll likely be able to fix that.

## Developers

While this code is reasonably well unit-tested, I was lazy and used real data for testing, which I can't make public. Don't let that prevent you from [filing pull requests](https://github.com/eawag-rdm/koboforms/pulls) though.
