`galcheat` data files
=====================

The following document describes the parameters expected for the photometric surveys and their filters: how they should be computed, their units, etc.

[**Survey parameters**](#survey-parameters) | [**Filter parameters**](#filter-parameters) | [**References**](#references) | [**Data file layout**](#yaml-file-layout)

Survey parameters
-----------------

### Units and types

| parameter name    | type  | units          |
| ----------------- | ----- | -------------- |
| name              | str   | –              |
| pixel_scale       | float | arcsec / pixel |
| gain              | float | e- / ADU       |
| mirror_diameter   | float | m              |
| obscuration       | float | dimensionless  |
| zeropoint_airmass | float | dimensionless  |

### Parameter description

#### `name`

The classical name or abbreviation for the survey. Most often this is how the survey is referred to.
In case of an ambiguity, for instance when a survey has several instruments, the name of the instrument should be added as a suffix (e.g. `Euclid_VIS`).

#### `description`

A bit of context around the survey: on which telescope, with which instrument, wide survey or a specific deep field.

#### `pixel_scale`

Size of a square pixel on the sky.

#### `gain`

Conversion factor between the photo-electrons received by the camera and the digital counts after the amplification of the electronics.

#### `mirror_diameter`

Primary mirror diameter, in meters.

#### `obscuration`

Proportion of the total area of the telescope that is obscured by the position of secondary mirrors, lenses, camera, etc.

This parameter is used to compute the effective area of the telescope.

#### `zeropoint_airmass`

Airmass value at which the zeropoint is computed.  
The airmass is commonly defined as the optical path length through the atmosphere relative to the zenith path length.
For space surveys, this value is set to 0.0.

Filter parameters
-----------------
### Units and types

| parameter name       | type      | units          |
| -------------------- | --------- | -------------- |
| name                 | str       | –              |
| sky_brightness       | float     | mag / arcsec^2 |
| full_exposure_time   | int/float | s              |
| zeropoint            | float     | mag            |
| psf_fwhm             | float     | arcsec         |
| effective_wavelength | float     | nm             |

### Description
#### `name`

Name of the filter

#### `sky_brightness`

Average sky brightness computed for the survey and this filter.  
The moon conditions under which this number was computed will be given as a comment in the yaml file.

#### `full_exposure_time`

Average exposure time of the filter on the same spot in the sky over the course of the survey.

#### `zeropoint`

The zeropoint is the magnitude of an object that produces 1 e- per second on the detector. It is computed for a given filter, using the [`speclite`][speclite] library with a classical atmosphere, at the airmass indicated in the survey parameters: `zeropoint_airmass`.


[speclite]: https://github.com/desihub/speclite

#### `psf_fwhm`

Average full width at half-maximum (FWHM) of the point spread function (PSF) over the filter.

#### `effective_wavelength` – ***optional***

Wavelength computed as a weighted average of the full passband throughput over the wavelength range.  
The throughput takes into account the transmission of the filter, the transmittance of the optics, the CCD efficiency as well as a standard atmospheric extinction model.

References
----------

The parameters written in `galcheat` have all been sourced and referenced.

These references can be specified for each parameter as a link and a comment string.

YAML file layout
----------------

The information for a given survey should be written in an individual YAML file, with a specific layout.

The survey information should appear first, with one parameter per line.

After these parameters, the list of filters should appear. YAML uses new lines and indentation to create lists.

An example for a survey called `Survey42` with two filters `a` and `b` is shown below.

```yaml
# Content of Survey42.yaml
name: "Survey42"
description: "The Survey42 was done on the XXX telescope with the YYY instrument"
pixel_scale: 0.2
gain: 2.0
mirror_diameter: 4.2
obscuration: 0.2
zeropoint_airmass: 1.2
filters:
  a:
    name: "a"
    sky_brightness: 19.4
    full_exposure_time: 500
    zeropoint: 26.90
    psf_fwhm: 1.1
    effective_wavelength: 500.00
  b:
    name: "b"
    sky_brightness: 18.6
    full_exposure_time: 500
    zeropoint: 27.36
    psf_fwhm: 1.2
    effective_wavelength: 600.00
references:
  pixel_scale:
    link: "https://link-to-the-pixelscale-ref.com"
    comment: "See section 2.4"
  gain:
    link: "https://link-to-the-gain-info.org"
    comment: ""
  psf_fwhm:
    link: "https://link-to-filters-refs.org"
    comment: ""
# goal is to have a reference per parameter, survey or filter-wise...
```
