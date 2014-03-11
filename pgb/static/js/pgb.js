$(document).ready(function() {
  var b = new Browser({
    chr:          '22',
    viewStart:    30000000,
    viewEnd:      30030000,
    cookieKey:    'human-grc_h37',

    coordSystem: {
      speciesName: 'Human',
      taxon: 9606,
      auth: 'GRCh',
      version: '37',
      ucscName: 'hg19'
    },

    chains: {
      hg18ToHg19: new Chainset('http://www.derkholm.net:8080/das/hg18ToHg19/', 'NCBI36', 'GRCh37',
                               {
                                  speciesName: 'Human',
                                  taxon: 9606,
                                  auth: 'NCBI',
                                  version: 36,
                                  ucscName: 'hg18'
                               })
    },

    sources: [{name: 'Genome',
               twoBitURI: 'http://www.biodalliance.org/datasets/hg19.2bit',
               tier_type: 'sequence'},
              {name: 'Genes',
               desc: 'Gene structures from GENCODE 19',
               bwgURI: 'http://www.biodalliance.org/datasets/gencode.bb',
               stylesheet_uri: 'http://www.biodalliance.org/stylesheets/gencode.xml',
               collapseSuperGroups: true,
               trixURI: 'http://www.biodalliance.org/datasets/geneIndex.ix'},
              {name: 'Conservation',
               desc: 'Conservation',
               bwgURI: 'http://www.biodalliance.org/datasets/phastCons46way.bw',
               noDownsample: true}],
    disablePoweredBy: true
  });

  $('a.variant').click(function() {
    b.setLocation($(this).attr("chr"),
                  parseInt($(this).attr("bp1"), 10),
                  parseInt($(this).attr("bp2"), 10));
  });
});
