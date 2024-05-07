from slitherin.detectors.arbitrary_call.arbitrary_call import ArbitraryCall
from slitherin.detectors.double_entry_token_possibility import (
    DoubleEntryTokenPossiblity,
)
from slitherin.detectors.dubious_typecast import DubiousTypecast
from slitherin.detectors.falsy_only_eoa_modifier import OnlyEOACheck
from slitherin.detectors.magic_number import MagicNumber
from slitherin.detectors.strange_setter import StrangeSetter
from slitherin.detectors.unprotected_setter import UnprotectedSetter
from slitherin.detectors.nft_approve_warning import NftApproveWarning
from slitherin.detectors.inconsistent_nonreentrant import InconsistentNonreentrant
from slitherin.detectors.call_forward_to_protected import CallForwardToProtected
from slitherin.detectors.multiple_storage_read import MultipleStorageRead
from slitherin.detectors.timelock_controller import TimelockController
from slitherin.detectors.tx_gasprice_warning import TxGaspriceWarning
from slitherin.detectors.unprotected_initialize import UnprotectedInitialize
from slitherin.detectors.read_only_reentrancy import ReadOnlyReentrancy
from slitherin.detectors.event_setter import EventSetter
from slitherin.detectors.before_token_transfer import BeforeTokenTransfer
from slitherin.detectors.uni_v2 import UniswapV2
from slitherin.detectors.token_fallback import TokenFallback
from slitherin.detectors.for_continue_increment import ForContinueIncrement
from slitherin.detectors.ecrecover import Ecrecover
from slitherin.detectors.public_vs_external import PublicVsExternal
from slitherin.detectors.aave.flashloan_callback import AAVEFlashloanCallbackDetector
from slitherin.detectors.arbitrum.arbitrum_prevrandao_difficulty import (
    ArbitrumPrevrandaoDifficulty,
)
from slitherin.detectors.arbitrum.block_number_timestamp import (
    ArbitrumBlockNumberTimestamp,
)
from slitherin.detectors.arbitrum.arbitrum_chainlink_price_feed import ArbitrumChainlinkPriceFeed
from slitherin.detectors.potential_arith_overflow import PotentialArithmOverflow
from slitherin.detectors.curve.curve_readonly_reentrancy import CurveReadonlyReentrancy
from slitherin.detectors.balancer.balancer_readonly_reentrancy import BalancerReadonlyReentrancy
from slitherin.detectors.vyper.reentrancy_curve_vyper_version import CurveVyperReentrancy
from slitherin.detectors.price_manipulation import PriceManipulationDetector

artbitrum_detectors = [
    ArbitrumPrevrandaoDifficulty,
    ArbitrumBlockNumberTimestamp,
    ArbitrumChainlinkPriceFeed
]

plugin_detectors = artbitrum_detectors + [
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
    AAVEFlashloanCallbackDetector,
    PotentialArithmOverflow,
    CurveReadonlyReentrancy,
    BalancerReadonlyReentrancy,
    CurveVyperReentrancy,
    PriceManipulationDetector
]
plugin_printers = []


def make_plugin():
    return plugin_detectors, plugin_printers
