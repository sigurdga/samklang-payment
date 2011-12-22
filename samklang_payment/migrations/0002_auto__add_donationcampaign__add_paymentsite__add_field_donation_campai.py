# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DonationCampaign'
        db.create_table('samklang_payment_donationcampaign', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samklang_payment.PaymentSite'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=80)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('test_mode', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('target_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('total_donations', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('other_donations', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=2, blank=True)),
            ('thank_you_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('thank_you_text_html', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('started', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('samklang_payment', ['DonationCampaign'])

        # Adding model 'PaymentSite'
        db.create_table('samklang_payment_paymentsite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('site', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['sites.Site'], unique=True)),
            ('default_currency', self.gf('django.db.models.fields.CharField')(default='NOK', max_length=3)),
            ('merchant_id', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('test_key', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('production_key', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
        ))
        db.send_create_signal('samklang_payment', ['PaymentSite'])

        # Adding field 'Donation.campaign'
        db.add_column('samklang_payment_donation', 'campaign', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['samklang_payment.DonationCampaign'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'DonationCampaign'
        db.delete_table('samklang_payment_donationcampaign')

        # Deleting model 'PaymentSite'
        db.delete_table('samklang_payment_paymentsite')

        # Deleting field 'Donation.campaign'
        db.delete_column('samklang_payment_donation', 'campaign_id')


    models = {
        'samklang_payment.donation': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Donation'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samklang_payment.DonationCampaign']", 'null': 'True', 'blank': 'True'}),
            'captured': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'transaction': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'blank': 'True'})
        },
        'samklang_payment.donationcampaign': {
            'Meta': {'object_name': 'DonationCampaign'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'other_donations': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'payment_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['samklang_payment.PaymentSite']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'started': ('django.db.models.fields.DateTimeField', [], {}),
            'target_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'test_mode': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'thank_you_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'thank_you_text_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'total_donations': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'samklang_payment.paymentsite': {
            'Meta': {'object_name': 'PaymentSite'},
            'default_currency': ('django.db.models.fields.CharField', [], {'default': "'NOK'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'merchant_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'production_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['sites.Site']", 'unique': 'True'}),
            'test_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'})
        },
        'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['samklang_payment']
