
import sys
import traceback
from   coriolis.Hurricane  import DbU, Breakpoint
from   coriolis            import Cfg
from   coriolis.CRL        import AllianceFramework, Blif, Catalog
from   coriolis.helpers    import loadUserSettings, setTraceLevel, overlay, trace, l, u, n
from   coriolis.helpers.io import ErrorMessage, WarningMessage, catch
loadUserSettings()
from   coriolis            import plugins
from   coriolis.plugins.block.block          import Block
from   coriolis.plugins.block.configuration  import IoPin, GaugeConf
from   coriolis.plugins.block.spares         import Spares
from   coriolis.plugins.core2chip.gf180mcu   import CoreToChip
from   coriolis.plugins.chip.configuration   import ChipConf
from   coriolis.plugins.chip.chip            import Chip


af = AllianceFramework.get()


def scriptMain ( **kw ):
    """The mandatory function to be called by Coriolis CGT/Unicorn."""
    with overlay.CfgCache(priority=Cfg.Parameter.Priority.UserFile) as cfg:
        cfg.misc.catchCore     = False
        cfg.misc.minTraceLevel = 15900
        cfg.misc.maxTraceLevel = 16000
        cfg.misc.info          = False
        cfg.misc.paranoid      = False
        cfg.misc.bug           = False
        cfg.misc.verboseLevel1 = True
        cfg.misc.verboseLevel2 = False
        cfg.misc.logMode       = True
        cfg.etesian.graphics   = 2

    global af
    rvalue = True
    try:
        #setTraceLevel( 550 )
        #Breakpoint.setStopLevel( 100 )
        buildChip    = True
        cg           = af.getCellGauge()
        sliceHeight  = cg.getSliceHeight()
        cell, editor = plugins.kwParseMain( **kw )
        topName      = 'cv32e40p_core'
        if 'loadCell' in kw: topName = kw[ 'loadCell' ]
        cell = af.getCell( topName, Catalog.State.Logical )
        if not cell:
            cell = Blif.load( topName )
        if editor:
            editor.setCell( cell ) 
            editor.setDbuMode( DbU.StringModePhysical )
        ioPadsSpec = [ (IoPin.WEST , None, 'clk_i'        , 'clk_i'          , 'clk_i'  )
                     , (IoPin.WEST , None, 'rst_ni'       , 'rst_ni'         , 'rst_ni' )
                     , (IoPin.WEST , None, 'boot_addr_i_{}', 'boot_addr_i({})', 'boot_addr_i({})' , 32 )
                     , (IoPin.WEST , None, 'allpower_0'   , 'DVDD'           , 'vdd'    )
                     , (IoPin.WEST , None, 'allground_0'  , 'DVSS'           , 'vss'    )

                     , (IoPin.SOUTH, None, 'mtvec_addr_i_{}', 'mtvec_addr_i({})' , 'mtvec_addr_i({})', 32 )
                     , (IoPin.SOUTH, None, 'allpower_1'     , 'DVDD'            , 'vdd'    )
                     , (IoPin.SOUTH, None, 'allground_1'    , 'DVSS'            , 'vss'    )

                     , (IoPin.EAST , None, 'dm_halt_addr_i_{}', 'dm_halt_addr_i({})', 'dm_halt_addr_i({})', 32 )
                     , (IoPin.EAST , None, 'allpower_2' , 'DVDD'   , 'vdd'    )
                     , (IoPin.EAST , None, 'allground_2', 'DVSS'   , 'vss'    )

                     , (IoPin.NORTH, None, 'hart_id_i_{}', 'hart_id_i({})', 'hart_id_i({})', 32 )
                     , (IoPin.NORTH, None, 'allpower_3' , 'DVDD'   , 'vdd'    )
                     , (IoPin.NORTH, None, 'allground_3', 'DVSS'   , 'vss'    )
                     ]
       #ioPinsSpec = [ (IoPin.WEST |IoPin.A_BEGIN, 'di({})'  , u(  13.0), u(13.0),  8)
       #             , (IoPin.WEST |IoPin.A_BEGIN, 'do({})'  , u( 117.0), u(13.0),  8)
       #             , (IoPin.EAST |IoPin.A_BEGIN, 'a({})'   , u(  13.0), u(13.0), 16)
       #             
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'clk'     , u(130.0),       0 ,  1)
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'irq'     , u(143.0),       0 ,  1)
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'nmi'     , u(156.0),       0 ,  1)
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'rdy'     , u(169.0),       0 ,  1)
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'we'      , u(182.0),       0 ,  1)
       #             , (IoPin.NORTH|IoPin.A_BEGIN, 'reset'   , u(195.0),       0 ,  1)
       #             ]
       #ioPinsSpec = []
        conf = ChipConf( cell, ioPins=[], ioPads=ioPadsSpec ) 
        conf.cfg.viewer.pixelThreshold       = 5
        conf.cfg.etesian.bloat               = 'disabled'
        conf.cfg.etesian.uniformDensity      = True
       # etesian.spaceMargin is ignored if the coreSize is directly set.
       #conf.cfg.etesian.aspectRatio         = 1.0
       #conf.cfg.etesian.spaceMargin         = 0.10
        conf.cfg.anabatic.searchHalo         = 2
        conf.cfg.anabatic.globalIterations   = 20
        conf.cfg.katana.hTracksReservedLocal = 6
        conf.cfg.katana.vTracksReservedLocal = 3
        conf.cfg.katana.hTracksReservedMin   = 4
        conf.cfg.katana.vTracksReservedMin   = 2
        conf.cfg.katana.trackFill            = 0
        conf.cfg.katana.runRealignStage      = True
        conf.cfg.block.spareSide             = 7*sliceHeight
        #conf.cfg.chip.minPadSpacing          = u(1.46)
        conf.cfg.chip.supplyRailWidth        = u(8.0)
        conf.cfg.chip.supplyRailPitch        = u(8.0)
        conf.editor              = editor
        conf.useSpares           = True
        conf.useClockTree        = True
        conf.useHFNS             = True
        conf.bColumns            = 2
        conf.bRows               = 2
        conf.chipName            = 'chip'
        conf.chipConf.ioPadGauge = 'LEF.GF_IO_Site'
        conf.coreToChipClass     = CoreToChip
        conf.coreSize            = ( 170*sliceHeight, 170*sliceHeight )
        conf.chipSize            = ( u( 3400.0), u( 3400.0) )
        if buildChip:
            conf.useHTree( 'clk_i_from_pad', Spares.HEAVY_LEAF_LOAD )
            chipBuilder = Chip( conf )
            chipBuilder.doChipNetlist()
            chipBuilder.doChipFloorplan()
            rvalue = chipBuilder.doPnR()
            chipBuilder.save()
        else:
            conf.useHTree( 'clk_i', Spares.HEAVY_LEAF_LOAD )
            blockBuilder = Block( conf )
            rvalue = blockBuilder.doPnR()
            blockBuilder.save()
    except Exception as e:
        catch( e )
        rvalue = False
    sys.stdout.flush()
    sys.stderr.flush()
    return rvalue


if __name__ == '__main__':
    rvalue = scriptMain()
    shellRValue = 0 if rvalue else 1
    sys.exit( shellRValue )
