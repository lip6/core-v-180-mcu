
import os
from   pathlib import Path
from   coriolis.designflow.technos import setupGf180mcu_c4m

if 'GITHUB_WORKFLOW' in os.environ:
    pdkMasterTop = Path('../../openpdks-c4m-gf180mcu/C4M.gf180mcu')
else:
    pdkMasterTop = Path('/usr/share/open_pdks/C4M.gf180mcu')
setupGf180mcu_c4m( checkToolkit=Path('..'), pdkMasterTop=pdkMasterTop )

DOIT_CONFIG = { 'verbosity' : 2 }

from coriolis                     import CRL
from coriolis.designflow.pnr      import PnR
from coriolis.designflow.sv2v     import Sv2v
from coriolis.designflow.svase    import Svase
from coriolis.designflow.surelog  import Surelog
from coriolis.designflow.yosys    import Yosys
from coriolis.designflow.blif2vst import Blif2Vst
from coriolis.designflow.alias    import Alias
from coriolis.designflow.clean    import Clean
PnR.textMode  = True


class Cv32e40pFiles ( object ):
    """
    Defines the SystemVerilog various files and directories needed to translate
    to Verilog the ``cv32e40p`` (RISC-V core) only.

    It provides the following attributes:

    ================  =========================================================
    Attribute         Provided information
    ================  =========================================================
    ``self.defines``  A list of macros to be defined.
    ``self.incdirs``  A list of directories for the ``include`` statement to
                      search in.
    ``self.libdirs``  A list of directories to search for libraries.
    ``self.svFiles``  The set of SystemVerilog & Verilog files to be compiled.
    ================  =========================================================
    """

    @staticmethod
    def filterOut ( rawSvFiles ):
        stemExcludes = [ 'cv32e40p_core_log'
                       , 'cv32e40p_register_file_latch'
                       , 'cv32e40p_prefetch_controller_sva'
                       ]
        svFiles = []
        for svFile in rawSvFiles:
            if svFile.stem in stemExcludes:
                print( '          X {}'.format(svFile) )
                continue
            svFiles.append( svFile )
        return svFiles

    @staticmethod
    def getFiles ( rtlRootDir, pathPattern ):
        rawSVFiles = sorted( rtlRootDir.glob( pathPattern ) )
        return Cv32e40pFiles.filterOut( rawSVFiles )

    @staticmethod
    def getSystemVerilogFiles ( rtlRootDir ):
        rtlRootDir = Path( rtlRootDir )
        print( '     - "{}".'.format( rtlRootDir ))
        svFiles  = Cv32e40pFiles.getFiles( rtlRootDir, '*.v' )
        svFiles += Cv32e40pFiles.getFiles( rtlRootDir, '*.sv' )
        return svFiles

    def __init__ ( self, rtlRootDir ):
        print( '  o  SystemVerilog/Verilog files of cv32e40p "{}"'.format( rtlRootDir ))
        self.defines    = [ 'TOVERILOG', 'SYNTHESIS', 'DISABLE_EFPGA' ]
        self.incdirs    = [ './rtl/vendor/openhwgroup_cv32e40p/bhv'
                          , './rtl/vendor/pulp_platform_common_cells/include'
                          , './rtl/vendor/pulp_platform_register_interface/include'
                          ]
        self.libdirs    = [ './rtl/vendor/openhwgroup_cv32e40p'
                          , './rtl/vendor/openhwgroup_cv32e40p/bhv'
                          , './rtl/vendor/openhwgroup_cv32e40p/rtl/include'
                          , './rtl/vendor/openhwgroup_cv32e40p/rtl'
                          , './rtl/vendor/openhwgroup_cv32e40p/sva'
                          ]
        self.svFiles    = []
        for libdir in self.libdirs:
            self.svFiles += Cv32e40pFiles.getSystemVerilogFiles( libdir )


class CoreVFiles ( object ):
    """
    Defines the SystemVerilog various files and directories needed to translate
    to Verilog a CORE-V MCU.

    It provides the following attributes:

    ================  =========================================================
    Attribute         Provided information
    ================  =========================================================
    ``self.defines``  A list of macros to be defined.
    ``self.incdirs``  A list of directories for the ``include`` statement to
                      search in.
    ``self.libdirs``  A list of directories to search for libraries.
    ``self.svFiles``  The set of SystemVerilog & Verilog files to be compiled.
    ================  =========================================================
    """

    @staticmethod
    def filterOut ( rawSvFiles ):
        stemExcludes = [ 'apb_efpga_demux'
                       , 'cv32e40p_core_log'
                       ]
        pathExcludes = [ 'fpga'
                       , '_latch'
                       , 'simulation'
                       , 'deprecated'
                       , 'BRIDGE'
                       , 'AddressDecoder'
                       , 'Arbitration'
                       , 'FanInPrimitive'
                       , 'Arbitration'
                       , 'Arbitration'
                       , 'XBAR'
                       ]
        svFiles = []
        for svFile in rawSvFiles:
            if svFile.stem in stemExcludes:
                print( '          X {}'.format(svFile) )
                continue
            matched = False
            for exclude in pathExcludes:
                if svFile.as_posix().find( exclude ) >= 0:
                    print( '       X {}'.format(svFile) )
                    matched = True
                    break
            if matched:
                continue
            svFiles.append( svFile )
        return svFiles

    @staticmethod
    def getFiles ( rtlRootDir, pathPattern ):
        rawSVFiles = sorted( rtlRootDir.glob( pathPattern ) )
        return CoreVFiles.filterOut( rawSVFiles )

    @staticmethod
    def getSystemVerilogFiles ( rtlRootDir ):
        rtlRootDir = Path( rtlRootDir )
        print( '     - "{}".'.format( rtlRootDir ))
        svFiles  = CoreVFiles.getFiles( rtlRootDir, '*.v' )
        svFiles += CoreVFiles.getFiles( rtlRootDir, '*.sv' )
        return svFiles

    def __init__ ( self, rtlRootDir ):
        print( '  o  SystemVerilog/Verilog files of CORE-V "{}"'.format( rtlRootDir ))
        self.defines    = [ 'TOVERILOG', 'SYNTHESIS', 'DISABLE_EFPGA' ]
        self.incdirs    = [ './rtl/includes'
                          , './rtl/core-v-mcu/include'
                          , './rtl/vendor/openhwgroup_cv32e40p/bhv'
                          , './rtl/vendor/pulp_platform_axi/include'
                          , './rtl/vendor/pulp_platform_common_cells/include'
                          , './rtl/vendor/pulp_platform_register_interface/include'
                          ]
        self.libdirs    = [ './rtl/L2_tcdm_hybrid_interco/RTL'
                          , './rtl/L2_tcdm_hybrid_interco/RTL/XBAR_BRIDGE'
                          , './rtl/L2_tcdm_hybrid_interco/RTL/XBAR_L2'
                          , './rtl/L2_tcdm_hybrid_interco/RTL/axi_2_lint'
                          , './rtl/apb2apbcomp'
                          , './rtl/apb2per'
                          , './rtl/apb_adv_timer/rtl'
                          , './rtl/apb_fll_if'
                          , './rtl/apb_gpio/rtl'
                          , './rtl/apb_i2cs/rtl'
                          , './rtl/apb_node/src'
                          , './rtl/apb_timer_unit/rtl'
                          , './rtl/axi_slice/src'
                          , './rtl/common_verification/src'
                          , './rtl/core-v-mcu/components'
                          , './rtl/core-v-mcu/efpga_subsystem'
                          , './rtl/core-v-mcu/fc'
                          , './rtl/core-v-mcu/soc'
                          , './rtl/core-v-mcu/top'
                          , './rtl/core-v-mcu/udma_subsystem'
                         #, './rtl/efpga'
                         #, './rtl/efpga/ql_fcb/rtl'
                         #, './rtl/efpga/ql_math_unit/rtl'
                          , './rtl/generic_FLL'
                          , './rtl/generic_FLL/fe/fpga'
                          , './rtl/generic_FLL/fe/model'
                          , './rtl/generic_FLL/fe/rtl'
                          , './rtl/logint_dc_fifo_xbar'
                          , './rtl/tcdm_interconnect/src'
                          , './rtl/udma/udma_camera/rtl'
                          , './rtl/udma/udma_core/rtl/common'
                          , './rtl/udma/udma_core/rtl/core'
                          , './rtl/udma/udma_external_per/rtl'
                          , './rtl/udma/udma_filter/rtl'
                          , './rtl/udma/udma_i2c/rtl'
                          , './rtl/udma/udma_i2s/rtl'
                          , './rtl/udma/udma_qspi/rtl'
                          , './rtl/udma/udma_sdio/rtl'
                          , './rtl/udma/udma_uart/rtl'
                          , './rtl/vendor/openhwgroup_cv32e40p'
                          , './rtl/vendor/openhwgroup_cv32e40p/bhv'
                          , './rtl/vendor/openhwgroup_cv32e40p/rtl/include'
                          , './rtl/vendor/openhwgroup_cv32e40p/rtl'
                          , './rtl/vendor/openhwgroup_cv32e40p/sva'
                          , './rtl/vendor/pulp_platform_axi/src'
                          , './rtl/vendor/pulp_platform_common_cells'
                          , './rtl/vendor/pulp_platform_common_cells/formal'
                          , './rtl/vendor/pulp_platform_common_cells/src'
                          , './rtl/vendor/pulp_platform_fpnew/src'
                          , './rtl/vendor/pulp_platform_fpu_div_sqrt_mvp/hdl'
                          , './rtl/vendor/pulp_platform_register_interface/include/register_interface'
                          , './rtl/vendor/pulp_platform_register_interface/src'
                          , './rtl/vendor/pulp_platform_register_interface/vendor'
                          , './rtl/vendor/pulp_platform_register_interface/vendor/lowrisc_opentitan/src'
                          , './rtl/vendor/pulp_platform_riscv_dbg/debug_rom'
                          , './rtl/vendor/pulp_platform_riscv_dbg/src'
                          , './rtl/vendor/pulp_platform_tech_cells_generic/src'
                          , './rtl/vendor/pulp_platform_tech_cells_generic/src/fpga'
                          , './rtl/vendor/pulp_platform_tech_cells_generic/src/rtl'
                          , './rtl/vip'
                          , './rtl/vip/camera'
                          ]
        self.svFiles    = []
        for libdir in self.libdirs:
            self.svFiles += CoreVFiles.getSystemVerilogFiles( libdir )


class UVMFiles ( object ):
    """
    Defines the SystemVerilog various files and directories needed to use
    the UVM framework. We use the ``VCS`` for data transaction (more or less
    randomly choosen as we need one).

    It provides the following attributes:

    ================  =========================================================
    Attribute         Provided information
    ================  =========================================================
    ``self.defines``  A list of macros to be defined.
    ``self.incdirs``  A list of directories for the ``include`` statement to
                      search in.
    ``self.libdirs``  A list of directories to search for libraries.
    ``self.svFiles``  The set of SystemVerilog & Verilog files to be compiled.
    ================  =========================================================
    """

    def __init__ ( self ):
        self.defines = [ 'VCS', 'UVM_NO_DPI' ]
        self.incdirs = [ Path( 'UVM' ) ]
        self.libdirs = [ ]
        self.svFiles = [ Path( 'UVM/uvm_pkg.sv' ) ]
    

from doDesign  import scriptMain

svTranslator = 'sv2v'
if 'SV_TRANSLATOR' in os.environ:
    svTranslator = os.environ['SV_TRANSLATOR'].lower()

buildChip = True
buildCv32 = True
if buildCv32:
    svObjects = [ Cv32e40pFiles( 'rtl' ) ]
   #topName = 'cv32e40p_aligner'
   #topName = 'cv32e40p_alu_div'
   #topName = 'cv32e40p_alu'
   #topName = 'cv32e40p_apu_disp'
   #topName = 'cv32e40p_compressed_decoder'
   #topName = 'cv32e40p_controller'
    topName = 'cv32e40p_core'                # KO
   #topName = 'cv32e40p_cs_registers'
   #topName = 'cv32e40p_decoder'             # KO
   #topName = 'cv32e40p_ex_stage'
   #topName = 'cv32e40p_ff_one'
   #topName = 'cv32e40p_fifo'
   #topName = 'cv32e40p_hwloop_regs'
   #topName = 'cv32e40p_id_stage'            # KO
   #topName = 'cv32e40p_if_stage'            # KO / Yosys (\TRANSPARENT redefined)
   #topName = 'cv32e40p_int_controller'
   #topName = 'cv32e40p_load_store_unit'     # KO / Yosys (\TRANSPARENT redefined)
   #topName = 'cv32e40p_mult'
   #topName = 'cv32e40p_obi_interface'
   #topName = 'cv32e40p_popcnt'
   #topName = 'cv32e40p_prefetch_buffer'    # KO / Yosys (\TRANSPARENT redefined)
   #topName = 'cv32e40p_prefetch_controller'
   #topName = 'cv32e40p_register_file'      # _ff version.
   #topName = 'cv32e40p_sleep_unit'
              
   #topName = 'cv32e40p_top'
   #topName = 'cv32e40p_wrapper '            # KO
else:
    svObjects = [ UVMFiles(), CoreVFiles( 'rtl' ) ]
    topName   = 'core_v_mcu'

defines = []
incdirs = []
libdirs = []
svFiles = []
for svObject in svObjects:
    defines += svObject.defines
    incdirs += svObject.incdirs
    libdirs += svObject.libdirs
    svFiles += svObject.svFiles

if svTranslator == 'svase':
    topName   = 'cv32e40p_alu_div'
    ruleSV    = Svase.mkRule( 'svase'
                            , '{}.v'.format( topName )
                            , svFiles
                            , top=topName
                            , svargs =[ '--timescale=1ns/1ps' ]
                            , defines=defines
                            , incdirs=incdirs
                            , libdirs=libdirs
                            )
elif svTranslator == 'sv2v':
    ruleSV  = Sv2v.mkRule( 'sv2v'
                         , '{}.v'.format( topName )
                         , svFiles
                         , top=topName
                         , defines=defines
                         , incdirs=incdirs
                         , libdirs=libdirs
                         )
elif svTranslator == 'surelog':
    topName   = 'cv32e40p_alu_div'
    ruleSV    = Surelog.mkRule( 'surelog'
                              , svFiles
                              , top     =topName
                              , options =[ '-timescale=1ns/1ps' ]
                              , defines =[ 'DISABLE_EFPGA=1' ]
                              , incdirs =incdirs
                              , libdirs =libdirs
                              )
else:
    print( '[ERROR] Unsupported SV_TRANSLATOR value "{}" (sv2v,svase,surelog)'.format( svTranslator ))

if buildChip:
    pnrFiles = [ 'chip_r.gds'
               , 'chip_r.vst'
               , 'chip_r.spi'
               , 'chip.vst'
               , 'chip.spi'
               , 'corona_cts_r.vst'
               , 'corona_cts_r.spi'
               , 'corona.vst'
               , 'corona.spi'
               , '{}_cts.vst'.format( topName )
               , '{}_cts.spi'.format( topName )
               ]
else:
    pnrFiles = [ '{}_cts_r.gds'.format( topName )
               , '{}_cts_r.vst'.format( topName )
               , '{}_cts_r.spi'.format( topName )
               ]

ruleYosys = Yosys.mkRule( 'yosys', [ruleSV], blackboxes=[ 'pPLL02F.v' ] )
ruleB2V   = Blif2Vst.mkRule( 'b2v', [ '{}.vst'.format( topName ) ]
                                  , [ruleYosys]
                                  , flags=0 )
rulePnR   = PnR     .mkRule( 'pnr', pnrFiles
                                  , [ruleB2V]
                                  , scriptMain
                                  , topName=topName )
ruleCgt   = PnR     .mkRule( 'cgt' )
ruleGds   = Alias   .mkRule( 'gds', [rulePnR] )
ruleClean = Clean   .mkRule( [ 'lefRWarning.log', './slpp_all' ] )
