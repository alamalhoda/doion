/**
 * Listing document upload helper.
 * Standalone /api/upload/ is not part of the API contract.
 * Use POST /api/v1/listings/{id}/documents/ via ListingService.uploadDocument.
 */
import { ListingService } from '@/features/listings/services/listingService'

export class UploadService {
  static async uploadListingDocument(
    listingId: number | string,
    file: File,
    documentType: 'cheque_image' | 'id_document' | 'supplementary',
  ) {
    return ListingService.uploadDocument(listingId, file, documentType)
  }
}
