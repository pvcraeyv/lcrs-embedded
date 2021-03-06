"""
Test functions that invoke system commands
"""
import logging

logger = logging.getLogger(__name__)


def test_lspci():
    """
    This test is only mocked on CI
    """
    from lcrs_embedded import settings
    from lcrs_embedded.system.lspci import lspci_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()
    lspci_analysis(scan_result, mock=settings.IS_CI)

    if settings.IS_CI:
        for k, v in lspci_analysis.expected_results.items():  # @UndefinedVariable  # noqa
            assert v == scan_result[k]
    else:
        assert bool(scan_result.graphics_controller)
        assert bool(scan_result.wifi)
        assert bool(scan_result.ethernet)
        assert bool(scan_result.has_usb)


def test_dmesg():
    """
    This test is always mocked
    """
    from lcrs_embedded.system.dmesg import dmesg_analysis
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()

    dmesg_analysis(scan_result)
    for k, v in dmesg_analysis.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]


def test_dmidecode():
    """
    This test is always mocked
    """
    from lcrs_embedded.system.dmidecode import dmidecode_system
    from lcrs_embedded.system.dmidecode import dmidecode_baseboard
    from lcrs_embedded.system.dmidecode import dmidecode_chassis
    from lcrs_embedded.system.dmidecode import dmidecode_memory
    from lcrs_embedded.system.dmidecode import dmidecode_processor
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()

    dmidecode_system(scan_result)
    for k, v in dmidecode_system.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]

    dmidecode_baseboard(scan_result)
    for k, v in dmidecode_baseboard.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]

    dmidecode_chassis(scan_result)
    for k, v in dmidecode_chassis.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]

    dmidecode_memory(scan_result)
    for k, v in dmidecode_memory.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]

    dmidecode_processor(scan_result)
    for k, v in dmidecode_processor.expected_results.items():  # @UndefinedVariable  # noqa
        assert v == scan_result[k]


def test_proc():
    """
    This test is always mocked, CI cannot read /proc, but a part from that,
    we don't get consistent output to test in these files anyways.
    """
    from lcrs_embedded.system.proc import cpuinfo, cdrominfo
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()

    cpuinfo(scan_result)
    for k, v in cpuinfo.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]

    cdrominfo(scan_result)
    for k, v in cdrominfo.expected_results.items():  # @UndefinedVariable
        assert v == scan_result[k]

    scan_result = ScanResult()

    cpuinfo(scan_result, mock_failure="alkdjakldakldakl")

    assert scan_result.processor_family is None

    cdrominfo(scan_result, mock_failure="alkdjakldakldakl")

    assert scan_result.cdrom is False


def test_battery():
    """
    This test is always mocked, CI cannot read /proc, but a part from that,
    we don't get consistent output to test in these files anyways.
    """
    from lcrs_embedded.system.battery import bat0
    from lcrs_embedded.models import ScanResult

    scan_result = ScanResult()

    bat0(scan_result)

    assert scan_result.battery

    bat0(scan_result, mock_failure="akdasdlkj")

    assert not scan_result.battery


def test_cdrom_eject():
    """
    Naturally, this test is mocked, as most CIs and dev laptops don't have
    cdrom drives :)
    """
    from lcrs_embedded.system.cdrom_eject import eject
    from lcrs_embedded.models import ScanResult

    #: Assert everything is fine when CD-ROM present and command mocked
    scan_result = ScanResult(
        cdrom=True,
        cdrom_drive_name="test"
    )
    eject(scan_result)

    assert scan_result.cdrom_ejected

    #: FAILS: Assert everything is fine when CD-ROM present and command failure
    scan_result = ScanResult(
        cdrom=True,
        cdrom_drive_name="test"
    )
    eject(scan_result, mock_failure="akdasdlkj")

    assert not scan_result.cdrom_ejected

    #: Assert everything is fine when no CD-ROM present
    scan_result = ScanResult()
    eject(scan_result)

    assert not scan_result.cdrom_ejected


def test_smartctl():
    """
    This test is always mocked, CI cannot read /proc, but a part from that,
    we don't get consistent output to test in these files anyways.
    """
    from lcrs_embedded.system.smartctl import smartinfo, expected_results
    from lcrs_embedded.models import ScanResult, Harddrive

    #: Assert everything is fine when CD-ROM present and command mocked
    scan_result = ScanResult(
        harddrives=[
            Harddrive(dev="sdz")
        ]
    )
    smartinfo(scan_result)

    assert scan_result.harddrives[0].smart_raw

    for k, v in expected_results.items():
        assert v == scan_result.harddrives[0][k]


def test_command_timeout():
    """
    This test is always mocked
    """
    from lcrs_embedded.utils.decorators import run_command

    @run_command("sleep 10", timeout=0.2)
    def test(stdout, stderr, succeeded):
        assert not succeeded

    test()
