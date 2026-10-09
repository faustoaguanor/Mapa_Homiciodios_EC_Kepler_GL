/* Aplicación del mapa: monta Kepler.gl (modo solo lectura, vista dividida)
 * y carga los datos incrustados por scripts/build.py (window.MAPA_DATA, window.MAPA_CONFIG). */
(function () {
  'use strict';

  /* Kepler.gl (deck.gl) necesita WebGL: si el navegador lo tiene desactivado,
   * se avisa en lugar de dejar que falle con "An error in deck.gl". */
  function hasWebGL() {
    try {
      var c = document.createElement('canvas');
      return Boolean(c.getContext('webgl2') || c.getContext('webgl'));
    } catch (e) {
      return false;
    }
  }
  if (!hasWebGL()) {
    document.getElementById('webglWarning').hidden = false;
    return;
  }

  var reducers = Redux.combineReducers({
    keplerGl: KeplerGl.keplerGlReducer.initialState({
      uiState: {readOnly: true, currentModal: null},
      mapState: {
        latitude: -2.709767451930464,
        longitude: -78.51181348434898,
        zoom: 5.78288143094078,
        bearing: 0,
        pitch: 0,
        isSplit: true
      }
    })
  });
  var store = Redux.createStore(
    reducers,
    {},
    Redux.applyMiddleware.apply(null, KeplerGl.enhanceReduxMiddleware([]))
  );

  /* Control de mapa personalizado: añade el botón de efectos */
var CustomMapControlFactory = (function createCustomMapControl(react, keplerGl) {
  var EffectControlFactory = keplerGl.EffectControlFactory;
  var EffectManagerFactory = keplerGl.EffectManagerFactory;
  var MapControlFactory = keplerGl.MapControlFactory;

  if (!EffectControlFactory || !EffectManagerFactory || !MapControlFactory) {
    console.warn('kepler.gl: Effect factories not available, skipping effect control injection');
    return null;
  }

  function EffectMapControlFactory(EffectControl, EffectManager) {
    var args = Array.prototype.slice.call(arguments, 2);
    var MapControl = MapControlFactory.apply(null, args);
    var actionComponents = (MapControl.defaultActionComponents || []).concat([EffectControl]);

    var EffectMapControl = function EffectMapControl(props) {
      var showEffects = Boolean(props.mapControls && props.mapControls.effect && props.mapControls.effect.active);
      return react.createElement(
        'div',
        {style: {
          position: 'absolute',
          display: 'flex',
          top: (props.top || 0) + 'px',
          right: 0,
          zIndex: 1,
          maxHeight: '100%',
          pointerEvents: 'none'
        }},
        react.createElement(
          'div',
          {style: {position: 'relative', pointerEvents: 'all'}},
          react.createElement(MapControl, Object.assign({}, props, {top: 0, actionComponents: actionComponents}))
        ),
        showEffects
          ? react.createElement('div', {
              style: {
                maxHeight: '100%',
                overflow: 'hidden',
                display: 'flex',
                flexDirection: 'column',
                pointerEvents: 'all',
                marginTop: '10px'
              }
            }, react.createElement(EffectManager, null))
          : null
      );
    };

    return EffectMapControl;
  }
  EffectMapControlFactory.deps = [EffectControlFactory, EffectManagerFactory].concat(MapControlFactory.deps);

  return [MapControlFactory, EffectMapControlFactory];
}(React, KeplerGl));

  var KeplerGlComponent = CustomMapControlFactory
    ? KeplerGl.injectComponents([CustomMapControlFactory])
    : KeplerGl.KeplerGl;

  function App() {
    var _s = React.useState({width: window.innerWidth, height: window.innerHeight});
    var dim = _s[0], setDim = _s[1];
    React.useEffect(function () {
      function onResize() { setDim({width: window.innerWidth, height: window.innerHeight}); }
      window.addEventListener('resize', onResize);
      return function () { window.removeEventListener('resize', onResize); };
    }, []);
    return React.createElement(
      'div',
      {style: {position: 'absolute', left: 0, width: '100vw', height: '100vh'}},
      React.createElement(KeplerGlComponent, {id: 'map', width: dim.width, height: dim.height})
    );
  }

  ReactDOM.createRoot(document.getElementById('app')).render(
    React.createElement(ReactRedux.Provider, {store: store}, React.createElement(App, null))
  );

  /* Carga de datos: GeoJSON y CSV -> formato interno de Kepler.gl */
  var datasets = window.MAPA_DATA.map(function (d) {
    return {
      info: {id: d.id, label: d.label},
      data: d.format === 'csv' ? KeplerGl.processCsvData(d.content) : KeplerGl.processGeojson(d.content)
    };
  });
  var config = KeplerGl.KeplerGlSchema.parseSavedConfig(window.MAPA_CONFIG);

  // Kepler.gl reinicia la configuración si se despacha antes de terminar el montaje
  window.setTimeout(function () {
    store.dispatch(KeplerGl.addDataToMap({datasets: datasets, config: config, options: {centerMap: false}}));
  }, 500);

  /* Panel lateral */
  var sidebar = document.getElementById('moranSidebar');
  var tab = document.getElementById('moranTab');
  tab.addEventListener('click', function () {
    var open = sidebar.classList.toggle('open');
    tab.setAttribute('aria-expanded', String(open));
  });
})();
