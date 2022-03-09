import astropy.units as u

from galcheat.filter import Filter
from galcheat.helpers import get_survey
from galcheat.survey import Survey


def mag2counts(magnitude, survey, filter):
    """Convert source magnitude to counts for a given filter of a survey

    To perform the computation, we use the filter zeropoint computed
    with `speclite` under classical atmospheric conditions and at a
    given airmass and we integrate over the survey lifetime using the
    full filter exposure time.

    Expect a rough estimate from this calculation since e.g. it does not
    take into account the atmospheric extinction. Therefore the result
    is casted to an integer.

    Parameters
    ----------
    magnitude: float
        magnitude of source
    survey: str or Survey
        Name of a given survey or Survey instance
    filter: str or Filter
        Name of the survey filter or Filter instance

    Returns
    -------
    The corresponding flux in counts

    References
    ----------
    The `WeakLensingDeblending` package
    https://github.com/LSSTDESC/WeakLensingDeblending

    """
    if not isinstance(magnitude, u.Quantity):
        magnitude *= u.mag(u.ct / u.s)
    else:
        magnitude = magnitude.value * u.mag(u.ct / u.s)

    if not isinstance(survey, Survey):
        survey = get_survey(survey)

    if not isinstance(filter, Filter):
        filter = survey.get_filter(filter)

    flux = (magnitude - filter.zeropoint).to(u.ct / u.s)
    counts = flux * filter.exposure_time

    return counts.astype(int)


def mean_sky_level(survey, filter):
    """Computes the mean sky level for a given survey and a filter

    This computation uses the sky brightness parameter from galcheat,
    expressed as a magnitude per square arcminute, weights it by the
    pixel area and converts it to counts.

    Parameters
    ----------
    survey: str or Survey
        Name of a given survey or Survey instance
    filter: str or Filter
        Name of the survey filter of Filter instance

    Returns
    -------
    The corresponding mean sky level in counts

    """
    if not isinstance(survey, Survey):
        survey = get_survey(survey)

    if not isinstance(filter, Filter):
        filter = survey.get_filter(filter)

    sky_brightness_counts = mag2counts(filter.sky_brightness, survey, filter)
    pixel_area = survey.pixel_scale.to_value(u.arcsec) ** 2

    mean_sky_level = sky_brightness_counts * pixel_area

    return mean_sky_level
