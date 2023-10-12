from slither_pess.detectors.arbitrary_call import ArbitraryCall
from slither_pess.detectors.double_entry_token_possibility import (
    DoubleEntryTokenPossiblity,
)
from slither_pess.detectors.dubious_typecast import DubiousTypecast
from slither_pess.detectors.falsy_only_eoa_modifier import OnlyEOACheck
from slither_pess.detectors.magic_number import MagicNumber
from slither_pess.detectors.strange_setter import StrangeSetter
from slither_pess.detectors.unprotected_setter import UnprotectedSetter
from slither_pess.detectors.nft_approve_warning import NftApproveWarning
from slither_pess.detectors.inconsistent_nonreentrant import InconsistentNonreentrant
from slither_pess.detectors.call_forward_to_protected import CallForwardToProtected
from slither_pess.detectors.multiple_storage_read import MultipleStorageRead
from slither_pess.detectors.timelock_controller import TimelockController
from slither_pess.detectors.tx_gasprice_warning import TxGaspriceWarning
from slither_pess.detectors.unprotected_initialize import UnprotectedInitialize
from slither_pess.detectors.read_only_reentrancy import ReadOnlyReentrancy
from slither_pess.detectors.event_setter import EventSetter
from slither_pess.detectors.before_token_transfer import BeforeTokenTransfer
from slither_pess.detectors.uni_v2 import UniswapV2
from slither_pess.detectors.token_fallback import TokenFallback
from slither_pess.detectors.for_continue_increment import ForContinueIncrement
from slither_pess.detectors.ecrecover import Ecrecover
from slither_pess.detectors.public_vs_external import PublicVsExternal


def make_plugin():
    plugin_detectors = [
        DoubleEntryTokenPossiblity,
        UnprotectedSetter,
        NftApproveWarning,
        InconsistentNonreentrant,
        StrangeSetter,
        OnlyEOACheck,
        MagicNumber,
        DubiousTypecast,
        CallForwardToProtected,
        MultipleStorageRead,
        TimelockController,
        TxGaspriceWarning,
        UnprotectedInitialize,
        ReadOnlyReentrancy,
        EventSetter,
        BeforeTokenTransfer,
        UniswapV2,
        TokenFallback,
        ForContinueIncrement,
        ArbitraryCall,
        Ecrecover,
        PublicVsExternal,
    ]
    plugin_printers = []

    return plugin_detectors, plugin_printers
