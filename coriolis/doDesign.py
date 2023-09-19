
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
#from   coriolis.plugins.core2chip.libresocio import CoreToChip
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
       #setTraceLevel( 540 )
       #Breakpoint.setStopLevel( 100 )
        buildChip    = False
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
       #ioPadsSpec = [ (IoPin.WEST , None, 'iopower_0'  , 'iovdd'  )
       #             , (IoPin.WEST , None, 'ioground_0' , 'vss'    )
       #             , (IoPin.WEST , None, 'di_0'       , 'di(0)'  , 'di(0)'  )
       #             , (IoPin.WEST , None, 'di_1'       , 'di(1)'  , 'di(1)'  )
       #             , (IoPin.WEST , None, 'di_2'       , 'di(2)'  , 'di(2)'  )
       #             , (IoPin.WEST , None, 'di_3'       , 'di(3)'  , 'di(3)'  )
       #             , (IoPin.WEST , None, 'power_0'    , 'vdd'    )
       #             , (IoPin.WEST , None, 'ground_0'   , 'vss'    )
       #             , (IoPin.WEST , None, 'di_4'       , 'di(4)'  , 'di(4)'  )
       #             , (IoPin.WEST , None, 'di_5'       , 'di(5)'  , 'di(5)'  )
       #             , (IoPin.WEST , None, 'di_6'       , 'di(6)'  , 'di(6)'  )
       #             , (IoPin.WEST , None, 'di_7'       , 'di(7)'  , 'di(7)'  )
       #             , (IoPin.WEST , None, 'ioground_1' , 'vss'    )
       #             , (IoPin.WEST , None, 'iopower_1'  , 'iovdd'  )
       #
       #             , (IoPin.SOUTH, None, 'iopower_2'  , 'iovdd'  )
       #             , (IoPin.SOUTH, None, 'ioground_2' , 'vss'    )
       #             , (IoPin.SOUTH, None, 'do_0'       , 'do(0)'  , 'do(0)'  )
       #             , (IoPin.SOUTH, None, 'do_1'       , 'do(1)'  , 'do(1)'  )
       #             , (IoPin.SOUTH, None, 'do_2'       , 'do(2)'  , 'do(2)'  )
       #             , (IoPin.SOUTH, None, 'do_3'       , 'do(3)'  , 'do(3)'  )
       #             , (IoPin.SOUTH, None, 'do_4'       , 'do(4)'  , 'do(4)'  )
       #             , (IoPin.SOUTH, None, 'do_5'       , 'do(5)'  , 'do(5)'  )
       #             , (IoPin.SOUTH, None, 'do_6'       , 'do(6)'  , 'do(6)'  )
       #             , (IoPin.SOUTH, None, 'do_7'       , 'do(7)'  , 'do(7)'  )
       #             , (IoPin.SOUTH, None, 'a_0'        , 'a(0)'   , 'a(0)'   )
       #             , (IoPin.SOUTH, None, 'a_1'        , 'a(1)'   , 'a(1)'   )
       #             , (IoPin.SOUTH, None, 'iopower_3'  , 'iovdd'  )
       #             , (IoPin.SOUTH, None, 'ioground_3' , 'vss'    )
       #
       #             , (IoPin.EAST , None, 'iopower_4'  , 'iovdd'  )
       #             , (IoPin.EAST , None, 'ioground_4' , 'vss'    )
       #             , (IoPin.EAST , None, 'a_2'        , 'a(2)'   , 'a(2)'   )
       #             , (IoPin.EAST , None, 'a_3'        , 'a(3)'   , 'a(3)'   )
       #             , (IoPin.EAST , None, 'a_4'        , 'a(4)'   , 'a(4)'   )
       #             , (IoPin.EAST , None, 'a_5'        , 'a(5)'   , 'a(5)'   )
       #             , (IoPin.EAST , None, 'a_6'        , 'a(6)'   , 'a(6)'   )
       #             , (IoPin.EAST , None, 'a_7'        , 'a(7)'   , 'a(7)'   )
       #             , (IoPin.EAST , None, 'power_1'    , 'vdd'    )
       #             , (IoPin.EAST , None, 'ground_1'   , 'vss'    )
       #             , (IoPin.EAST , None, 'a_8'        , 'a(8)'   , 'a(8)'   )
       #             , (IoPin.EAST , None, 'a_9'        , 'a(9)'   , 'a(9)'   )
       #             , (IoPin.EAST , None, 'a_10'       , 'a(10)'  , 'a(10)'  )
       #             , (IoPin.EAST , None, 'a_11'       , 'a(11)'  , 'a(11)'  )
       #             , (IoPin.EAST , None, 'a_12'       , 'a(12)'  , 'a(12)'  )
       #             , (IoPin.EAST , None, 'a_13'       , 'a(13)'  , 'a(13)'  )
       #             , (IoPin.EAST , None, 'ioground_5' , 'vss'    )
       #             , (IoPin.EAST , None, 'iopower_5'  , 'iovdd'  )
       #
       #             , (IoPin.NORTH, None, 'iopower_6'  , 'iovdd'  )
       #             , (IoPin.NORTH, None, 'ioground_6' , 'vss'    )
       #             , (IoPin.NORTH, None, 'irq'        , 'irq'    , 'irq'    )
       #             , (IoPin.NORTH, None, 'nmi'        , 'nmi'    , 'nmi'    )
       #             , (IoPin.NORTH, None, 'rdy'        , 'rdy'    , 'rdy'    )
       #             , (IoPin.NORTH, None, 'power_2'    , 'vdd'    )
       #             , (IoPin.NORTH, None, 'ground_2'   , 'vss'    )
       #             , (IoPin.NORTH, None, 'clk'        , 'clk'    , 'clk'    )
       #             , (IoPin.NORTH, None, 'reset'      , 'reset'  , 'reset'  )
       #             , (IoPin.NORTH, None, 'we'         , 'we'     , 'we'     )
       #             , (IoPin.NORTH, None, 'a_14'       , 'a(14)'  , 'a(14)'  )
       #             , (IoPin.NORTH, None, 'a_15'       , 'a(15)'  , 'a(15)'  )
       #             , (IoPin.NORTH, None, 'ioground_7' , 'vss'    )
       #             , (IoPin.NORTH, None, 'iopower_7'  , 'iovdd'  )
       #             ]
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
        conf = ChipConf( cell, ioPins=[], ioPads=[] ) 
        conf.cfg.viewer.pixelThreshold       = 5
        conf.cfg.etesian.bloat               = 'disabled'
        conf.cfg.etesian.uniformDensity      = True
       # etesian.spaceMargin is ignored if the coreSize is directly set.
       #conf.cfg.etesian.aspectRatio         = 1.0
       #conf.cfg.etesian.spaceMargin         = 0.10
        conf.cfg.anabatic.searchHalo         = 2
        conf.cfg.anabatic.globalIterations   = 20
        conf.cfg.anabatic.topRoutingLayer    = 'Metal5'
        conf.cfg.katana.hTracksReservedLocal = 6
        conf.cfg.katana.vTracksReservedLocal = 3
        conf.cfg.katana.hTracksReservedMin   = 3
        conf.cfg.katana.vTracksReservedMin   = 1
        conf.cfg.katana.trackFill            = 0
        conf.cfg.katana.runRealignStage      = True
        conf.cfg.block.spareSide             = 7*sliceHeight
       #conf.cfg.chip.padCoreSide            = 'North'
       #conf.cfg.chip.use45corners           = False
        conf.cfg.chip.useAbstractPads        = False
        conf.cfg.chip.minPadSpacing          = u(1.46)
        conf.cfg.chip.supplyRailWidth        = u(8.0)
        conf.cfg.chip.supplyRailPitch        = u(8.0)
        conf.editor              = editor
        conf.useSpares           = True
        conf.useClockTree        = True
        conf.useHFNS             = False
        conf.bColumns            = 2
        conf.bRows               = 2
        conf.chipName            = 'chip'
        #conf.chipConf.ioPadGauge = 'LibreSOCIO'
        conf.coreToChipClass     = None
        # 29 is minimum with everything disabled       -> ~  6% free space.
        # Can really be reached when running the P&R on the sole block.
        # This is very suspicious.
        # 33 is minimum for obstacle density           -> ~ 25% free space.
        # 34 is minimum for cell packing near obstacle -> ~ 30% free space.
        conf.coreSize            = ( 170*sliceHeight, 170*sliceHeight )
        conf.chipSize            = ( u( 2020.0), u( 2060.0) )
        conf.useHTree( 'clk_i', Spares.HEAVY_LEAF_LOAD )
        #conf.useHTree( 'core.subckt_0_cpu.abc_11829_new_n340' )
        if buildChip:
            chipBuilder = Chip( conf )
            chipBuilder.doChipNetlist()
            chipBuilder.doChipFloorplan()
            rvalue = chipBuilder.doPnR()
            chipBuilder.save()
        else:
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
